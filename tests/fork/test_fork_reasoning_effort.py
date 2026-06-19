"""Tests for the per-subagent reasoning_effort feature."""

import pytest
import inspect


def test_delegate_task_accepts_reasoning_effort():
    """delegate_task() should accept a reasoning_effort parameter."""
    from tools.delegate_tool import delegate_task

    sig = inspect.signature(delegate_task)
    assert "reasoning_effort" in sig.parameters, (
        "delegate_task should accept a reasoning_effort parameter"
    )


def test_reasoning_effort_passed_through():
    """reasoning_effort should be forwarded to subagent tasks."""
    from tools.delegate_tool import delegate_task
    import inspect

    sig = inspect.signature(delegate_task)
    has_reasoning = "reasoning_effort" in sig.parameters
    assert has_reasoning, "delegate_task() should accept reasoning_effort"

    # Check default value
    param = sig.parameters["reasoning_effort"]
    assert param.default is None or param.default == inspect.Parameter.empty, (
        "reasoning_effort should default to None"
    )


def test_reasoning_config_translated_to_api_params():
    """ProviderProfile.build_api_kwargs_extras should translate reasoning_config."""
    from providers.base import ProviderProfile

    profile = ProviderProfile(name="test")

    # Provide reasoning_config settings with high effort
    reasoning_config = {
        "enabled": True,
        "effort": "high",
        "max_thinking_tokens": 8192,
    }
    extra_body, top_level = profile.build_api_kwargs_extras(reasoning_config=reasoning_config)

    # Should produce extra_body with thinking (enabled) and reasoning (high effort)
    assert "thinking" in extra_body, "extra_body should contain thinking"
    assert extra_body["thinking"]["type"] == "enabled", (
        "thinking should be enabled"
    )
    assert "reasoning" in extra_body, "extra_body should contain reasoning"
    assert extra_body["reasoning"]["enabled"] is True, (
        "reasoning should be enabled"
    )
    assert extra_body["reasoning"]["effort"] == "high", (
        "reasoning effort should be 'high'"
    )


def test_reasoning_config_disabled():
    """Disabled reasoning config should produce disabled thinking."""
    from providers.base import ProviderProfile

    profile = ProviderProfile(name="test")

    reasoning_config = {
        "enabled": False,
    }
    extra_body, top_level = profile.build_api_kwargs_extras(reasoning_config=reasoning_config)

    assert extra_body["thinking"]["type"] == "disabled", (
        "thinking should be disabled when reasoning is disabled"
    )
    assert extra_body["reasoning"]["enabled"] is False, (
        "reasoning should be disabled"
    )
    assert "chat_template_kwargs" in extra_body, (
        "should include chat_template_kwargs for vLLM compatibility"
    )
