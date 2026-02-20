"""
THUNDERFIRE AutoGen Tools

Provides tool registration for AutoGen agents.
"""

import json
from typing import Optional

from ..client import ThunderFireClientSync
from ..types import TOOLS


class ThunderFireAutoGen:
    """AutoGen tool registration for THUNDERFIRE."""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.client = ThunderFireClientSync(api_url, api_key)

    def register_tools(self, agent):
        """Register all 16 THUNDERFIRE tools with an AutoGen agent."""

        # Create wrapper functions for each tool
        def node_list() -> str:
            """List all connected THUNDERFIRE autonomous nodes."""
            return json.dumps(self.client.node_list())

        def node_health(node_id: str) -> str:
            """Get CHITRAL health for a node."""
            return json.dumps(self.client.node_health(node_id))

        def node_create(name: str, class_type: str, tier: int) -> str:
            """Create a new THUNDERFIRE node."""
            return json.dumps(self.client.node_create(name, class_type, tier))

        def marketplace_search(query: str, category: str = None) -> str:
            """Search TF Store marketplace."""
            return json.dumps(self.client.marketplace_search(query, category))

        def marketplace_install(package_name: str, version: str = None, node_id: str = None) -> str:
            """Install a package from TF Store."""
            return json.dumps(self.client.marketplace_install(package_name, version, node_id))

        def chitral_decode(hex_str: str) -> str:
            """Decode a CHITRAL hex message."""
            return json.dumps(self.client.chitral_decode(hex_str))

        def chitral_status(node_id: str) -> str:
            """Get CHITRAL status for a node."""
            return json.dumps(self.client.chitral_status(node_id))

        def theta_run(node_id: str, stage: int = None, params: dict = None) -> str:
            """Execute a THETA decision cycle."""
            return json.dumps(self.client.theta_run(node_id, stage, params))

        def theta_status(node_id: str) -> str:
            """Get THETA status for a node."""
            return json.dumps(self.client.theta_status(node_id))

        def service_discover(category: str = None, min_tier: int = None) -> str:
            """Discover NOP services."""
            return json.dumps(self.client.service_discover(category, min_tier))

        def service_request(service_id: str, params: dict = None) -> str:
            """Request a NOP service."""
            return json.dumps(self.client.service_request(service_id, params))

        def gym_tasks() -> str:
            """List GYM tasks."""
            return json.dumps(self.client.gym_tasks())

        def gym_complete(task_id: str, result: dict) -> str:
            """Complete a GYM task."""
            return json.dumps(self.client.gym_complete(task_id, result))

        def msg_send(channel: str, recipient: str, text: str) -> str:
            """Send a message via NOP."""
            return json.dumps(self.client.msg_send(channel, recipient, text))

        def msg_history(channel: str, limit: int = 20) -> str:
            """Get message history."""
            return json.dumps(self.client.msg_history(channel, limit))

        def script_eval(code: str, node_id: str = None) -> str:
            """Execute TOP Script."""
            return json.dumps(self.client.script_eval(code, node_id))

        # Register each tool
        tool_funcs = {
            "thunderfire_node_list": node_list,
            "thunderfire_node_health": node_health,
            "thunderfire_node_create": node_create,
            "thunderfire_marketplace_search": marketplace_search,
            "thunderfire_marketplace_install": marketplace_install,
            "thunderfire_chitral_decode": chitral_decode,
            "thunderfire_chitral_status": chitral_status,
            "thunderfire_theta_run": theta_run,
            "thunderfire_theta_status": theta_status,
            "thunderfire_service_discover": service_discover,
            "thunderfire_service_request": service_request,
            "thunderfire_gym_tasks": gym_tasks,
            "thunderfire_gym_complete": gym_complete,
            "thunderfire_msg_send": msg_send,
            "thunderfire_msg_history": msg_history,
            "thunderfire_script_eval": script_eval,
        }

        for tool_def in TOOLS:
            func = tool_funcs.get(tool_def.name)
            if func:
                try:
                    agent.register_for_llm(
                        name=tool_def.name,
                        description=tool_def.description
                    )(func)
                except AttributeError:
                    # Fallback for different AutoGen versions
                    pass

    def get_tool_functions(self) -> dict:
        """Return tool functions for manual registration."""
        return {
            "thunderfire_node_list": lambda: json.dumps(self.client.node_list()),
            "thunderfire_node_health": lambda node_id: json.dumps(self.client.node_health(node_id)),
            "thunderfire_node_create": lambda name, class_type, tier: json.dumps(
                self.client.node_create(name, class_type, tier)
            ),
            "thunderfire_marketplace_search": lambda query, category=None: json.dumps(
                self.client.marketplace_search(query, category)
            ),
            "thunderfire_marketplace_install": lambda package_name, version=None, node_id=None: json.dumps(
                self.client.marketplace_install(package_name, version, node_id)
            ),
            "thunderfire_chitral_decode": lambda hex_str: json.dumps(self.client.chitral_decode(hex_str)),
            "thunderfire_chitral_status": lambda node_id: json.dumps(self.client.chitral_status(node_id)),
            "thunderfire_theta_run": lambda node_id, stage=None, params=None: json.dumps(
                self.client.theta_run(node_id, stage, params)
            ),
            "thunderfire_theta_status": lambda node_id: json.dumps(self.client.theta_status(node_id)),
            "thunderfire_service_discover": lambda category=None, min_tier=None: json.dumps(
                self.client.service_discover(category, min_tier)
            ),
            "thunderfire_service_request": lambda service_id, params=None: json.dumps(
                self.client.service_request(service_id, params)
            ),
            "thunderfire_gym_tasks": lambda: json.dumps(self.client.gym_tasks()),
            "thunderfire_gym_complete": lambda task_id, result: json.dumps(
                self.client.gym_complete(task_id, result)
            ),
            "thunderfire_msg_send": lambda channel, recipient, text: json.dumps(
                self.client.msg_send(channel, recipient, text)
            ),
            "thunderfire_msg_history": lambda channel, limit=20: json.dumps(
                self.client.msg_history(channel, limit)
            ),
            "thunderfire_script_eval": lambda code, node_id=None: json.dumps(
                self.client.script_eval(code, node_id)
            ),
        }
