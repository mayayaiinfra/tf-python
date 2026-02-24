#!/usr/bin/env python3
"""
THUNDERFIRE OpenAI Assistant Example

Using OpenAI function calling with THUNDERFIRE tools via the provider-agnostic API.

This example demonstrates the new thunderfire.llm provider interface, which supports
multiple LLM providers (OpenAI, Anthropic, Local). The provider is auto-detected from
environment variables.

Usage:
    export THUNDERFIRE_API_KEY=tf_live_...
    export OPENAI_API_KEY=sk-...
    python openai_assistant.py

Provider Support:
    - OpenAI: Set OPENAI_API_KEY
    - Anthropic: Set ANTHROPIC_API_KEY (use with Anthropic SDK instead of OpenAI SDK)
    - Local: Set STREAM_LOCAL_URL (use with OpenAI-compatible local inference)
"""

import os
import sys
import json


def main():
    # Check for API keys
    if not os.environ.get("THUNDERFIRE_API_KEY"):
        print("Error: THUNDERFIRE_API_KEY environment variable required")
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable required")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("Install dependencies: pip install openai")
        sys.exit(1)

    from thunderfire import ThunderFireClientSync
    from thunderfire.llm import get_provider

    # Initialize clients
    print("Initializing clients...")
    openai_client = OpenAI()
    tf_client = ThunderFireClientSync()

    # Get provider (auto-detects OpenAI from OPENAI_API_KEY)
    provider = get_provider("openai", client=tf_client)
    tools = provider.get_tool_definitions()
    print(f"Loaded {len(tools)} THUNDERFIRE tools (provider: {provider.provider_name})")

    # Initial message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that manages THUNDERFIRE autonomous nodes. "
                      "Use the available tools to help users monitor and manage their node fleet."
        },
        {
            "role": "user",
            "content": "List all my connected nodes and check if any have health below 90%."
        }
    ]

    print("\n--- Starting Conversation ---")
    print(f"User: {messages[-1]['content']}\n")

    # Conversation loop
    max_iterations = 5
    for i in range(max_iterations):
        # Call OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Check if we're done
        if not assistant_message.tool_calls:
            print(f"Assistant: {assistant_message.content}")
            break

        # Add assistant message to history
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in assistant_message.tool_calls
            ]
        })

        # Handle tool calls
        for tool_call in assistant_message.tool_calls:
            print(f"[Calling {tool_call.function.name}...]")

            result = provider.handle_tool_call(tool_call)
            tool_message = provider.create_tool_response(tool_call.id, result)
            messages.append(tool_message)

            # Pretty print result
            print(f"  Result: {json.dumps(result, indent=2)[:200]}...")

    print("\n--- Conversation Complete ---")


if __name__ == "__main__":
    main()
