#!/usr/bin/env python3
"""
THUNDERFIRE CrewAI Crew Example

A crew of agents that monitor and maintain an autonomous node fleet.

Usage:
    export THUNDERFIRE_API_KEY=tf_live_...
    export OPENAI_API_KEY=sk-...
    python crewai_crew.py
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
        from crewai import Agent, Crew, Task
    except ImportError:
        print("Install dependencies: pip install crewai")
        sys.exit(1)

    from thunderfire.crewai import ThunderFireTools

    # Create THUNDERFIRE tools
    print("Initializing THUNDERFIRE tools...")
    tf = ThunderFireTools()
    tools = tf.get_tools()
    print(f"Loaded {len(tools)} THUNDERFIRE tools")

    # Create agents
    fleet_manager = Agent(
        role="Fleet Manager",
        goal="Monitor autonomous node fleet and ensure all nodes are healthy",
        backstory="You are an experienced fleet manager responsible for monitoring "
                  "and maintaining a fleet of autonomous THUNDERFIRE nodes.",
        tools=tools,
        verbose=True
    )

    diagnostics_agent = Agent(
        role="Diagnostics Specialist",
        goal="Diagnose issues with nodes and recommend solutions",
        backstory="You are a diagnostics specialist who analyzes CHITRAL health data "
                  "and identifies potential issues with autonomous nodes.",
        tools=tools,
        verbose=True
    )

    # Create tasks
    monitor_task = Task(
        description="List all connected nodes and identify any with health below 80%.",
        expected_output="A report listing all nodes and their health status, "
                       "with any unhealthy nodes highlighted.",
        agent=fleet_manager
    )

    diagnose_task = Task(
        description="For any nodes with health below 80%, run a detailed health check "
                   "and recommend corrective actions.",
        expected_output="A diagnosis report with specific recommendations for each unhealthy node.",
        agent=diagnostics_agent,
        context=[monitor_task]
    )

    # Create and run crew
    print("\n--- Starting Crew ---")
    crew = Crew(
        agents=[fleet_manager, diagnostics_agent],
        tasks=[monitor_task, diagnose_task],
        verbose=True
    )

    result = crew.kickoff()

    # Print result
    print("\n--- Crew Result ---")
    print(result)


if __name__ == "__main__":
    main()
