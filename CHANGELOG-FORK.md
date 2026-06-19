# Hermes Fork Changelog

## Custom Changes

### [2026-06-18] Per-Subagent Reasoning Effort + Config Write Bypass
- **Commit:** `39c841f01`
- **Files:** `providers/base.py`, `tools/delegate_tool.py`, `tools/file_tools.py`
- **Description:** Added reasoning_effort param to delegate_task(), HERMES_ALLOW_CONFIG_WRITE env var bypass for config safety check, API reasoning params (thinking/reasoning/chat_template_kwargs in extra_body) in default provider profile
- **Tests:** `tests/fork/test_fork_reasoning_effort.py`, `tests/fork/test_fork_config_write_bypass.py`
- **Status:** ✅ Active

## Upstream Merges

### [2026-06-19] Merged upstream/main (16 commits)
- **Status:** ✅ Merged and tested
- **Upstream commits:**
  - `c02192ff6` feat(image-gen): add image-to-image / editing to image_generate (#48705)
  - `cfb55de5e` Update Stripe Projects skill docs (#48673)
  - `e4452ff8b` fix(agent): summarize structured provider error messages
  - `620fd59b8` feat(model-picker): add Refresh Models control to bust stale model cache (#48691)
  - `28d887ca1` Merge pull request #48615 from NousResearch/fix/dashboard-ds-button-api
  - `d06104a9e` fix(dashboard): resolve chat TUI argv off event loop (#48561)
  - `8568988b0` chore: add JoaoMarcos44 to AUTHOR_MAP
  - `e48554a3e` feat(cli): lock hermes worktrees so concurrent processes can't clobber them
  - `62c71ebd8` chore(release): map chanyoung.kim@nota.ai -> channkim for #47049 salvage
  - `1d2e35967` fix(cli): surface a visible warning when the session store is unavailable
  - `9ae98e07a` fix(agent): rebuild base fts without trigram
  - `c10aa5dc9` fix(agent): address review feedback on trigram tokenizer fallback
  - `0403f41f9` fix(agent): handle missing trigram tokenizer without disabling FTS5
  - `2c6e266e8` fix(relay): trigger self-provision on relay-config + NAS token, not is_managed() (#48724)
  - `36851fa57` fix(docker): support WebUI installs from read-only sources (#48541)
  - `d573e7c9e` fix(dashboard): use DS Button prefix/size API instead of inline icons
- **Tests:** All fork tests passed
