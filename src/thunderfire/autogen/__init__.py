"""
THUNDERFIRE AutoGen Integration

Usage:
    from thunderfire.autogen import ThunderFireAutoGen
    from autogen import ConversableAgent

    tf = ThunderFireAutoGen(api_key="tf_live_...")
    assistant = ConversableAgent("fleet_manager", llm_config={...})
    tf.register_tools(assistant)
"""

from .tools import ThunderFireAutoGen

__all__ = ["ThunderFireAutoGen"]
