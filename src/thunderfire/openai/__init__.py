"""
THUNDERFIRE OpenAI Integration

DEPRECATED: Use `thunderfire.llm` for platform-agnostic provider support.

Legacy usage (still supported with deprecation warning):
    from thunderfire.openai import get_function_definitions, handle_tool_call
    from thunderfire import ThunderFireClient
    import openai

    client = ThunderFireClient(api_key="tf_live_...")
    tools = get_function_definitions()

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "List my nodes"}],
        tools=tools
    )

    for tool_call in response.choices[0].message.tool_calls:
        result = handle_tool_call(tool_call, client)

New usage (recommended):
    from thunderfire.llm import get_provider
    from thunderfire import ThunderFireClient
    import openai

    client = ThunderFireClient(api_key="tf_live_...")
    provider = get_provider("openai")  # or "anthropic", "local", "auto"
    tools = provider.get_tool_definitions()

    response = openai.chat.completions.create(...)
    for tool_call in response.choices[0].message.tool_calls:
        result = provider.handle_tool_call(tool_call)
"""

import warnings
from .functions import get_function_definitions as _get_function_definitions, handle_tool_call as _handle_tool_call


def get_function_definitions(*args, **kwargs):
    """DEPRECATED: Use thunderfire.llm.get_provider().get_tool_definitions() instead."""
    warnings.warn(
        "thunderfire.openai.get_function_definitions() is deprecated. "
        "Use thunderfire.llm.get_provider().get_tool_definitions() instead. "
        "See https://docs.thunderfire.ai/migration-guide for details.",
        DeprecationWarning,
        stacklevel=2
    )
    return _get_function_definitions(*args, **kwargs)


def handle_tool_call(*args, **kwargs):
    """DEPRECATED: Use thunderfire.llm.get_provider().handle_tool_call() instead."""
    warnings.warn(
        "thunderfire.openai.handle_tool_call() is deprecated. "
        "Use thunderfire.llm.get_provider().handle_tool_call() instead. "
        "See https://docs.thunderfire.ai/migration-guide for details.",
        DeprecationWarning,
        stacklevel=2
    )
    return _handle_tool_call(*args, **kwargs)


__all__ = ["get_function_definitions", "handle_tool_call"]
