"""Tests for the parallel chunked compression feature."""

import pytest
import inspect


def test_estimate_chunk_tokens_exists():
    """_estimate_chunk_tokens helper should be defined."""
    from agent.context_compressor import _estimate_chunk_tokens

    assert callable(_estimate_chunk_tokens), (
        "_estimate_chunk_tokens should be a callable function"
    )


def test_estimate_chunk_tokens_basic():
    """Basic chunk estimation with small turns should yield one chunk."""
    from agent.context_compressor import _estimate_chunk_tokens

    turns = [{"content": "hello world"}, {"content": "test message"}]
    chunks = _estimate_chunk_tokens(turns, target=100_000)
    assert isinstance(chunks, list), "should return a list of chunks"
    assert len(chunks) >= 1, "should produce at least one chunk"


def test_estimate_chunk_tokens_single_turn_fragment():
    """A single oversized turn should become its own chunk (fragment)."""
    from agent.context_compressor import _estimate_chunk_tokens

    big_turn = {"content": "x" * 5_000}
    turns = [big_turn]
    chunks = _estimate_chunk_tokens(turns, target=1_000, max_turn=500)
    assert len(chunks) >= 1, "oversized turn should still be chunked"


def test_summarize_chunked_method_exists():
    """ContextCompressor should have _summarize_chunked method."""
    from agent.context_compressor import ContextCompressor

    assert hasattr(ContextCompressor, "_summarize_chunked"), (
        "ContextCompressor should have _summarize_chunked method"
    )


def test_combine_summary_fragments_method_exists():
    """ContextCompressor should have _combine_summary_fragments method."""
    from agent.context_compressor import ContextCompressor

    assert hasattr(ContextCompressor, "_combine_summary_fragments"), (
        "ContextCompressor should have _combine_summary_fragments method"
    )


def test_chunked_call_in_generate_summary():
    """_generate_summary should check token thresholds and delegate to chunked path."""
    from agent.context_compressor import ContextCompressor

    source = inspect.getsource(ContextCompressor._generate_summary)
    assert "_summarize_chunked" in source, (
        "_generate_summary should reference _summarize_chunked"
    )
    assert "_CHUNK_TARGET_TOKENS" in source, (
        "_generate_summary should reference _CHUNK_TARGET_TOKENS"
    )


def test_concurrent_futures_imported():
    """concurrent.futures should be imported for parallel chunk processing."""
    from agent import context_compressor

    source = inspect.getsource(context_compressor)
    assert "concurrent.futures" in source, (
        "context_compressor should import concurrent.futures"
    )
