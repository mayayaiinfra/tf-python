"""
THUNDERFIRE CrewAI Integration

Usage:
    from thunderfire.crewai import ThunderFireTools
    from crewai import Agent, Crew, Task

    tf = ThunderFireTools(api_key="tf_live_...")
    agent = Agent(
        role="Fleet Manager",
        goal="Monitor and maintain autonomous node fleet",
        tools=tf.get_tools()
    )
"""

from .tools import ThunderFireTools

__all__ = ["ThunderFireTools"]
