"""
THUNDERFIRE Local Provider — Ollama/vLLM/llama.cpp (OpenAI-compatible).

Implements local inference with OpenAI-compatible function calling.
Works with: Ollama, vLLM, llama.cpp server, and other OpenAI-compatible endpoints.
"""

import json
import os
from typing import Any, Dict, List

from .base import ThunderFireLLMProvider
from ..types import TOOLS, TOOL_HANDLER_MAP
from ..client import ThunderFireClientSync


class LocalProvider(ThunderFireLLMProvider):
    """Local inference provider (OpenAI-compatible) for THUNDERFIRE tools.

    EDGE: Infrastructure-agnostic — works with any OpenAI-compatible endpoint.
    Base URL configured via STREAM_LOCAL_URL env var (default: http://localhost:11434).
    """

    def __init__(self, client: ThunderFireClientSync = None, base_url: str = None):
        """Initialize local provider.

        Args:
            client: ThunderFireClientSync instance (created if not provided)
            base_url: Base URL for local inference (default: from STREAM_LOCAL_URL env)
        """
        self._client = client or ThunderFireClientSync()
        self._base_url = base_url or os.getenv("STREAM_LOCAL_URL", "http://localhost:11434")

    @property
    def client(self) -> ThunderFireClientSync:
        return self._client

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def base_url(self) -> str:
        """Base URL for local inference endpoint."""
        return self._base_url

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return OpenAI-compatible function calling definitions.

        Local providers use OpenAI format (most are OpenAI-compatible):
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
        """Execute tool call from local inference response.

        Args:
            tool_call: OpenAI-compatible tool call object with:
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
        """Create OpenAI-compatible tool response message.

        OpenAI format (used by local providers):
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
