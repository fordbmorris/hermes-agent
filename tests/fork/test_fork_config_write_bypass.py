"""Tests for the HERMES_ALLOW_CONFIG_WRITE bypass feature."""

import os
import pytest
import inspect


def test_env_var_recognized():
    """The HERMES_ALLOW_CONFIG_WRITE env var should be checked by file_tools."""
    from tools.file_tools import _check_sensitive_path

    source = inspect.getsource(_check_sensitive_path)
    assert "HERMES_ALLOW_CONFIG_WRITE" in source, (
        "_check_sensitive_path should reference HERMES_ALLOW_CONFIG_WRITE"
    )


def test_sensitive_path_check_mentions_config():
    """_check_sensitive_path should reference config.yaml."""
    from tools.file_tools import _check_sensitive_path

    source = inspect.getsource(_check_sensitive_path)
    assert "config.yaml" in source, (
        "_check_sensitive_path should reference config.yaml"
    )
    assert "HERMES_ALLOW_CONFIG_WRITE" in source, (
        "_check_sensitive_path should reference HERMES_ALLOW_CONFIG_WRITE"
    )
