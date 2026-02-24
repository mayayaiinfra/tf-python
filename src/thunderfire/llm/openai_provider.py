"""
THUNDERFIRE OpenAI Provider — OpenAI function calling format.

Implements OpenAI-compatible function calling for THUNDERFIRE tools.
"""

import json
from typing import Any, Dict, List

from .base import ThunderFireLLMProvider
from ..types import TOOLS, TOOL_HANDLER_MAP
from ..client import ThunderFireClientSync


class OpenAIProvider(ThunderFireLLMProvider):
    """OpenAI function calling provider for THUNDERFIRE tools."""

    def __init__(self, client: ThunderFireClientSync = None):
        """Initialize OpenAI provider.

        Args:
            client: ThunderFireClientSync instance (created if not provided)
        """
        self._client = client or ThunderFireClientSync()

    @property
    def client(self) -> ThunderFireClientSync:
        return self._client

    @property
    def provider_name(self) -> str:
        return "openai"

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return OpenAI-compatible function calling definitions.

        OpenAI format:
          {
            "type": "function",
            "function": {
              "name": "chitral_status",
              "description": "Get node status...",
              "parameters": {"type": "object", "properties": {...}, "required": [...]}
            }
          }
        """
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

    def handle_tool_call(self, tool_call: Any) -> Dict[str, Any]:
        """Execute OpenAI tool call.

        Args:
            tool_call: ChatCompletionMessageToolCall object with:
              - id: Tool call ID
              - function.name: Tool name
              - function.arguments: JSON string with arguments

        Returns:
            Result dict from handler
        """
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        handler_name = TOOL_HANDLER_MAP.get(name)
        if not handler_name:
            return {"error": f"Unknown tool: {name}"}

        handler = getattr(self._client, handler_name, None)
        if not handler:
            return {"error": f"Handler not found: {handler_name}"}

        try:
            result = handler(**args)
            return result
        except Exception as e:
            return {"error": str(e)}

    def create_tool_response(self, tool_call_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create OpenAI tool response message.

        OpenAI format:
          {
            "role": "tool",
            "tool_call_id": "call_abc123",
            "content": "{\"result\": ...}"
          }
        """
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": json.dumps(result)
        }
