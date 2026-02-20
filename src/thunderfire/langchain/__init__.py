"""
THUNDERFIRE LangChain Integration

Usage:
    from thunderfire.langchain import ThunderFireToolkit
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    toolkit = ThunderFireToolkit(api_key="tf_live_...")
    tools = toolkit.get_tools()
    agent = create_react_agent(ChatOpenAI(), tools)
"""

from .toolkit import ThunderFireToolkit

__all__ = ["ThunderFireToolkit"]
