"""
THUNDERFIRE - Autonomous Node Framework for AI Agents

This package provides integrations for major AI agent frameworks:
- LLM: `from thunderfire.llm import get_provider` (platform-agnostic)
- LangChain: `from thunderfire.langchain import ThunderFireToolkit`
- CrewAI: `from thunderfire.crewai import ThunderFireTools`
- AutoGen: `from thunderfire.autogen import ThunderFireAutoGen`
- OpenAI: `from thunderfire.openai import get_function_definitions` (deprecated, use llm)
- MCP: `thunderfire-mcp` command or `from thunderfire.mcp import server`

Quick Start:
    from thunderfire import ThunderFireClient
    from thunderfire.llm import get_provider

    client = ThunderFireClient(api_key="tf_live_...")
    provider = get_provider()  # Auto-detects OpenAI/Anthropic/Local
    tools = provider.get_tool_definitions()
"""

__version__ = "1.0.0"

from .client import ThunderFireClient, ThunderFireClientSync
from .types import Node, NodeHealth, Package, Service, GymTask, Message

__all__ = [
    "__version__",
    "ThunderFireClient",
    "ThunderFireClientSync",
    "Node",
    "NodeHealth",
    "Package",
    "Service",
    "GymTask",
    "Message",
]
