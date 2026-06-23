"""Tests for the delegation effort_mapping feature (effort->model routing)."""

import pytest
import inspect


def test_build_child_agent_contains_effort_mapping():
    """_build_child_agent should reference effort_mapping."""
    from tools.delegate_tool import _build_child_agent

    source = inspect.getsource(_build_child_agent)
    assert "effort_mapping" in source, (
        "_build_child_agent should reference effort_mapping"
    )


def test_effort_mapping_parses_config_dict():
    """The effort_mapping block should look up delegation_cfg for a dict."""
    from tools.delegate_tool import _build_child_agent

    source = inspect.getsource(_build_child_agent)
    assert 'delegation_cfg.get("effort_mapping"' in source or (
        'delegation_cfg.get("effort_mapping")' in source
    ), (
        "effort_mapping should be read from delegation_cfg"
    )


def test_effort_mapping_overrides_model():
    """When effort keys match, model/provider/base_url/api_key should be overridable."""
    from tools.delegate_tool import _build_child_agent

    source = inspect.getsource(_build_child_agent)
    # The mapping block should reference these override points
    for attr in ["effective_model", "effective_provider", "effective_base_url", "effective_api_key"]:
        assert attr in source, (
            f"_build_child_agent should reference {attr} in effort mapping"
        )


def test_effort_mapping_extra_body():
    """effort_mapping entries can carry extra_body for child request overrides."""
    from tools.delegate_tool import _build_child_agent

    source = inspect.getsource(_build_child_agent)
    assert "child_request_overrides" in source, (
        "_build_child_agent should support child_request_overrides from effort mapping"
    )
