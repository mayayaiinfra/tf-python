#!/usr/bin/env python3
"""
THUNDERFIRE AutoGen Chat Example

An AutoGen conversation between a user proxy and a fleet manager agent.

Usage:
    export THUNDERFIRE_API_KEY=tf_live_...
    export OPENAI_API_KEY=sk-...
    python autogen_chat.py
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
        from autogen import ConversableAgent, UserProxyAgent
    except ImportError:
        print("Install dependencies: pip install autogen-agentchat")
        sys.exit(1)

    from thunderfire.autogen import ThunderFireAutoGen

    # Create THUNDERFIRE tools
    print("Initializing THUNDERFIRE tools...")
    tf = ThunderFireAutoGen()
    tool_funcs = tf.get_tool_functions()
    print(f"Loaded {len(tool_funcs)} THUNDERFIRE tools")

    # Create agents
    llm_config = {
        "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}],
        "timeout": 120
    }

    fleet_manager = ConversableAgent(
        name="FleetManager",
        system_message="You are a fleet manager for THUNDERFIRE autonomous nodes. "
                      "You can list nodes, check health, search the marketplace, "
                      "and manage GYM tasks. Be helpful and informative.",
        llm_config=llm_config
    )

    # Register tools manually
    for name, func in tool_funcs.items():
        fleet_manager.register_function(
            function_map={name: func}
        )

    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5
    )

    # Start conversation
    print("\n--- Starting Chat ---")
    user_proxy.initiate_chat(
        fleet_manager,
        message="Please list all connected THUNDERFIRE nodes and give me a summary of "
               "the fleet status. Then check if there are any GYM improvement tasks pending."
    )


if __name__ == "__main__":
    main()
