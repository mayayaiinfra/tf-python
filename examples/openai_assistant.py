#!/usr/bin/env python3
"""
THUNDERFIRE OpenAI Assistant Example

Using OpenAI function calling with THUNDERFIRE tools.

Usage:
    export THUNDERFIRE_API_KEY=tf_live_...
    export OPENAI_API_KEY=sk-...
    python openai_assistant.py
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
    from thunderfire.openai import get_function_definitions, handle_tool_call, create_tool_message

    # Initialize clients
    print("Initializing clients...")
    openai_client = OpenAI()
    tf_client = ThunderFireClientSync()
    tools = get_function_definitions()
    print(f"Loaded {len(tools)} THUNDERFIRE tools")

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

            result = handle_tool_call(tool_call, tf_client)
            messages.append(create_tool_message(tool_call.id, result))

            # Pretty print result
            try:
                parsed = json.loads(result)
                print(f"  Result: {json.dumps(parsed, indent=2)[:200]}...")
            except:
                print(f"  Result: {result[:200]}...")

    print("\n--- Conversation Complete ---")


if __name__ == "__main__":
    main()
