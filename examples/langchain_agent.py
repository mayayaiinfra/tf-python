#!/usr/bin/env python3
"""
THUNDERFIRE LangChain Agent Example

A ReAct agent that manages autonomous nodes using THUNDERFIRE tools.

This example uses ThunderFireToolkit, which provides LangChain-compatible tool wrappers.
The toolkit internally uses the provider-agnostic thunderfire.llm interface and will
auto-detect your LLM provider (OpenAI, Anthropic, Local) from environment variables.

Usage:
    export THUNDERFIRE_API_KEY=tf_live_...
    export OPENAI_API_KEY=sk-...
    python langchain_agent.py

Provider Support:
    The toolkit auto-detects your provider:
    - OpenAI: Set OPENAI_API_KEY (default)
    - Anthropic: Set ANTHROPIC_API_KEY
    - Local: Set STREAM_LOCAL_URL
"""

import os
import sys


def main():
    # Check for API keys
    if not os.environ.get("THUNDERFIRE_API_KEY"):
        print("Error: THUNDERFIRE_API_KEY environment variable required")
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable required")
        sys.exit(1)

    try:
        from langchain_openai import ChatOpenAI
        from langgraph.prebuilt import create_react_agent
    except ImportError:
        print("Install dependencies: pip install langchain-openai langgraph")
        sys.exit(1)

    from thunderfire.langchain import ThunderFireToolkit

    # Create THUNDERFIRE toolkit
    print("Initializing THUNDERFIRE toolkit...")
    toolkit = ThunderFireToolkit()
    tools = toolkit.get_tools()
    print(f"Loaded {len(tools)} THUNDERFIRE tools")

    # Create LangChain agent
    llm = ChatOpenAI(model="gpt-4o-mini")
    agent = create_react_agent(llm, tools)

    # Run the agent
    print("\n--- Agent Task ---")
    print("Task: List all connected nodes and check the health of the first one\n")

    result = agent.invoke({
        "messages": [
            ("user", "List all connected THUNDERFIRE nodes and check the health of the first one. "
                     "Report any issues you find.")
        ]
    })

    # Print result
    print("\n--- Agent Response ---")
    for message in result["messages"]:
        if hasattr(message, "content") and message.content:
            print(message.content)


if __name__ == "__main__":
    main()
