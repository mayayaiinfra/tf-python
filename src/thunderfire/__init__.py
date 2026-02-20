"""
THUNDERFIRE - Autonomous Node Framework for AI Agents

This package provides integrations for major AI agent frameworks:
- LangChain: `from thunderfire.langchain import ThunderFireToolkit`
- CrewAI: `from thunderfire.crewai import ThunderFireTools`
- AutoGen: `from thunderfire.autogen import ThunderFireAutoGen`
- OpenAI: `from thunderfire.openai import get_function_definitions`
- MCP: `thunderfire-mcp` command or `from thunderfire.mcp import server`

Quick Start:
    from thunderfire import ThunderFireClient

    client = ThunderFireClient(api_key="tf_live_...")
    nodes = await client.node_list()
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
