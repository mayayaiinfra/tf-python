"""
THUNDERFIRE OpenAI Integration

Usage:
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
"""

from .functions import get_function_definitions, handle_tool_call

__all__ = ["get_function_definitions", "handle_tool_call"]
