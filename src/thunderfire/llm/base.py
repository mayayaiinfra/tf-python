"""
THUNDERFIRE LLM Provider Base — Abstract interface for provider-agnostic tools.

EDGE: Platform-agnostic — same tool definitions work with any LLM provider.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ThunderFireLLMProvider(ABC):
    """Abstract LLM provider interface for THUNDERFIRE 16 tools.

    Each provider (OpenAI, Anthropic, Local) implements this interface
    to expose THUNDERFIRE tools in their native format.
    """

    @abstractmethod
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return tool definitions in this provider's native format.

        Returns:
            List of tool definitions (format varies by provider):
              - OpenAI: {"type": "function", "function": {...}}
              - Anthropic: {"name": "...", "description": "...", "input_schema": {...}}
              - Local: OpenAI-compatible format
        """
        pass

    @abstractmethod
    def handle_tool_call(self, tool_call: Any) -> Dict[str, Any]:
        """Execute a tool call from provider response.

        Args:
            tool_call: Provider-specific tool call object:
              - OpenAI: ChatCompletionMessageToolCall
              - Anthropic: ToolUseBlock (content block)
              - Local: ChatCompletionMessageToolCall (OpenAI-compatible)

        Returns:
            Result dict (raw result from THUNDERFIRE client handler)
        """
        pass

    @abstractmethod
    def create_tool_response(self, tool_call_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create tool response message in provider's format.

        Args:
            tool_call_id: Provider's tool call identifier
            result: Tool execution result dict

        Returns:
            Provider-specific message dict:
              - OpenAI: {"role": "tool", "tool_call_id": "...", "content": "..."}
              - Anthropic: {"role": "user", "content": [{"type": "tool_result", ...}]}
              - Local: OpenAI-compatible format
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return provider name (e.g., 'openai', 'anthropic', 'local')."""
        pass

    @property
    @abstractmethod
    def client(self):
        """Return the ThunderFireClientSync instance used by this provider."""
        pass
