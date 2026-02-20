"""
THUNDERFIRE OpenAI Function Definitions

Provides OpenAI-compatible function calling definitions.
"""

import json
from typing import Any

from ..types import TOOLS, TOOL_HANDLER_MAP
from ..client import ThunderFireClientSync


def get_function_definitions() -> list[dict]:
    """Return OpenAI-compatible function calling definitions for all 16 tools."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        }
        for tool in TOOLS
    ]


def handle_tool_call(tool_call: Any, client: ThunderFireClientSync) -> str:
    """
    Execute a tool call from OpenAI response.

    Args:
        tool_call: OpenAI ChatCompletionMessageToolCall object
        client: ThunderFireClientSync instance

    Returns:
        JSON string with tool result
    """
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    handler_name = TOOL_HANDLER_MAP.get(name)
    if not handler_name:
        return json.dumps({"error": f"Unknown tool: {name}"})

    handler = getattr(client, handler_name, None)
    if not handler:
        return json.dumps({"error": f"Handler not found: {handler_name}"})

    try:
        result = handler(**args)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


def create_tool_message(tool_call_id: str, result: str) -> dict:
    """Create a tool response message for OpenAI chat."""
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": result
    }
