#!/usr/bin/env bash
# fork-sync.sh — Fetch upstream, merge, test, log, push
set -euo pipefail

FORK_DIR="/usr/local/hermes-agent-dev"
VENV_PYTHON="$FORK_DIR/venv/bin/python"
UPSTREAM_BRANCH="upstream/main"
LOG="$FORK_DIR/CHANGELOG-FORK.md"

cd "$FORK_DIR"

# 1. Fetch upstream
echo "=== [1/5] Fetching upstream ==="
git fetch upstream

# 2. Check for new commits
NEW_COMMITS=$(git log HEAD..$UPSTREAM_BRANCH --oneline)
if [ -z "$NEW_COMMITS" ]; then
    echo "No new upstream commits. Nothing to do."
    exit 0
fi

echo ""
echo "=== New upstream commits ==="
echo "$NEW_COMMITS"
echo ""

# 3. Attempt merge
echo "=== [2/5] Merging upstream/main ==="
if git merge $UPSTREAM_BRANCH --no-edit 2>&1; then
    echo "✅ Merge clean"
else
    echo ""
    echo "❌ MERGE CONFLICT"
    echo "Conflicting files:"
    git diff --name-only --diff-filter=U
    git merge --abort
    echo ""
    echo "Merge aborted. Resolve conflicts manually, then:"
    echo "  git merge upstream/main"
    echo "  # resolve conflicts"
    echo "  git add . && git commit"
    echo "  pytest tests/fork/ -v"
    echo "  git push origin main"
    exit 1
fi

# 4. Run fork-specific tests
echo ""
echo "=== [3/5] Running fork test suite ==="
$VENV_PYTHON -m pytest tests/fork/ -v 2>&1
TEST_EXIT=$?

if [ $TEST_EXIT -ne 0 ]; then
    echo ""
    echo "❌ FORK TESTS FAILED after merge"
    echo "Rolling back merge..."
    git merge --abort
    echo "Merge aborted. Manual intervention required."
    exit 1
fi
echo "✅ All fork tests passed"

# 5. Log the merge in CHANGELOG-FORK.md
echo ""
echo "=== [4/5] Logging merge ==="
MERGE_DATE=$(date +%Y-%m-%d)
COMMIT_COUNT=$(echo "$NEW_COMMITS" | wc -l)
cat >> "$LOG" << EOF

### [$MERGE_DATE] Merged upstream/main ($COMMIT_COUNT commits)
- **Status:** ✅ Merged and tested
- **Upstream commits:**
$(echo "$NEW_COMMITS" | sed 's/^/  - `/;s/$/`/')
- **Tests:** All fork tests passed
EOF

git add "$LOG"
git commit -m "docs: log upstream merge of $COMMIT_COUNT commits"

# 6. Push to fork
echo ""
echo "=== [5/5] Pushing to origin ==="
git push origin main
echo ""
echo "✅ Sync complete — $COMMIT_COUNT upstream commits merged and pushed"
