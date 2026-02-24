"""
THUNDERFIRE Anthropic Provider — Anthropic tool_use format.

Implements Anthropic-compatible tool calling for THUNDERFIRE tools.
"""

import json
from typing import Any, Dict, List

from .base import ThunderFireLLMProvider
from ..types import TOOLS, TOOL_HANDLER_MAP
from ..client import ThunderFireClientSync


class AnthropicProvider(ThunderFireLLMProvider):
    """Anthropic tool_use provider for THUNDERFIRE tools."""

    def __init__(self, client: ThunderFireClientSync = None):
        """Initialize Anthropic provider.

        Args:
            client: ThunderFireClientSync instance (created if not provided)
        """
        self._client = client or ThunderFireClientSync()

    @property
    def client(self) -> ThunderFireClientSync:
        return self._client

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return Anthropic-compatible tool_use definitions.

        Anthropic format:
          {
            "name": "chitral_status",
            "description": "Get node status...",
            "input_schema": {
              "type": "object",
              "properties": {...},
              "required": [...]
            }
          }
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters  # Same as OpenAI parameters (JSON Schema)
            }
            for tool in TOOLS
        ]

    def handle_tool_call(self, tool_call: Any) -> Dict[str, Any]:
        """Execute Anthropic tool_use call.

        Args:
            tool_call: ToolUseBlock (content block) or dict with:
              - id: Tool use ID
              - name: Tool name
              - input: Dict with arguments

        Returns:
            Result dict from handler
        """
        # Handle both object and dict formats
        if hasattr(tool_call, 'name'):
            name = tool_call.name
            args = tool_call.input
        else:
            name = tool_call.get('name')
            args = tool_call.get('input', {})

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
        """Create Anthropic tool_result message.

        Anthropic format:
          {
            "role": "user",
            "content": [
              {
                "type": "tool_result",
                "tool_use_id": "toolu_abc123",
                "content": "{\"result\": ...}"
              }
            ]
          }
        """
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call_id,
                    "content": json.dumps(result)
                }
            ]
        }
