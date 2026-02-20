"""
THUNDERFIRE CrewAI Tools

Provides 16 tools as CrewAI @tool decorated functions.
"""

import json
from typing import Optional

from ..client import ThunderFireClientSync

try:
    from crewai import tool
except ImportError:
    raise ImportError(
        "CrewAI integration requires crewai. "
        "Install with: pip install thunderfire[crewai]"
    )


class ThunderFireTools:
    """CrewAI tools for THUNDERFIRE autonomous node management."""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self._client = ThunderFireClientSync(api_url, api_key)
        self._tools = self._create_tools()

    def _create_tools(self):
        """Create all tool instances."""
        client = self._client

        @tool("List THUNDERFIRE Nodes")
        def node_list() -> str:
            """List all connected autonomous nodes with IDs, tiers, and health status."""
            return json.dumps(client.node_list())

        @tool("Check Node Health")
        def node_health(node_id: str) -> str:
            """Get CHITRAL health for a node. Returns 7 status fields."""
            return json.dumps(client.node_health(node_id))

        @tool("Create Node")
        def node_create(name: str, class_type: str, tier: int) -> str:
            """Create a new THUNDERFIRE node with the specified configuration."""
            return json.dumps(client.node_create(name, class_type, int(tier)))

        @tool("Search Marketplace")
        def marketplace_search(query: str, category: str = None) -> str:
            """Search TF Store marketplace for packages."""
            return json.dumps(client.marketplace_search(query, category))

        @tool("Install Package")
        def marketplace_install(package_name: str, version: str = None, node_id: str = None) -> str:
            """Install a package from TF Store onto a node."""
            return json.dumps(client.marketplace_install(package_name, version, node_id))

        @tool("Decode CHITRAL")
        def chitral_decode(hex_str: str) -> str:
            """Decode a CHITRAL hex message into structured fields."""
            return json.dumps(client.chitral_decode(hex_str))

        @tool("CHITRAL Status")
        def chitral_status(node_id: str) -> str:
            """Get CHITRAL status summary for a node."""
            return json.dumps(client.chitral_status(node_id))

        @tool("Run THETA Cycle")
        def theta_run(node_id: str, stage: int = None) -> str:
            """Execute a THETA decision cycle on a node."""
            return json.dumps(client.theta_run(node_id, int(stage) if stage else None))

        @tool("THETA Status")
        def theta_status(node_id: str) -> str:
            """Get current THETA status for a node."""
            return json.dumps(client.theta_status(node_id))

        @tool("Discover Services")
        def service_discover(category: str = None, min_tier: int = None) -> str:
            """Discover available NOP services in the network."""
            return json.dumps(client.service_discover(category, int(min_tier) if min_tier else None))

        @tool("Request Service")
        def service_request(service_id: str) -> str:
            """Request a NOP service and begin negotiation."""
            return json.dumps(client.service_request(service_id))

        @tool("List GYM Tasks")
        def gym_tasks() -> str:
            """List GYM autonomous improvement tasks."""
            return json.dumps(client.gym_tasks())

        @tool("Complete GYM Task")
        def gym_complete(task_id: str, result: str) -> str:
            """Mark a GYM task as completed with results."""
            result_dict = json.loads(result) if isinstance(result, str) else result
            return json.dumps(client.gym_complete(task_id, result_dict))

        @tool("Send Message")
        def msg_send(channel: str, recipient: str, text: str) -> str:
            """Send a message via NOP communication channel."""
            return json.dumps(client.msg_send(channel, recipient, text))

        @tool("Message History")
        def msg_history(channel: str, limit: int = 20) -> str:
            """Get message history for a channel."""
            return json.dumps(client.msg_history(channel, int(limit)))

        @tool("Evaluate Script")
        def script_eval(code: str, node_id: str = None) -> str:
            """Execute a TOP Script on a node."""
            return json.dumps(client.script_eval(code, node_id))

        return [
            node_list, node_health, node_create,
            marketplace_search, marketplace_install,
            chitral_decode, chitral_status,
            theta_run, theta_status,
            service_discover, service_request,
            gym_tasks, gym_complete,
            msg_send, msg_history,
            script_eval
        ]

    def get_tools(self) -> list:
        """Return all 16 tools for CrewAI Crew."""
        return self._tools
