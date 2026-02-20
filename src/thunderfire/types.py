"""
THUNDERFIRE Type Definitions

Shared data classes for all framework integrations.
"""

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Node:
    """THUNDERFIRE autonomous node."""
    id: str
    name: str
    tier: int
    class_type: int
    health: int
    status: str


@dataclass
class NodeHealth:
    """CHITRAL health status (7 fields)."""
    capability: int
    health: int
    intent: int
    timeline: int
    resources: int
    authority: int
    lifecycle: int
    uptime: int
    cpu: int
    memory: int
    errors: int


@dataclass
class Package:
    """TF Store marketplace package."""
    name: str
    version: str
    description: str
    category: str
    downloads: int
    rating: float


@dataclass
class Service:
    """NOP service in the network."""
    id: str
    name: str
    category: str
    tier: int
    price: dict
    provider: str


@dataclass
class GymTask:
    """GYM autonomous improvement task."""
    id: str
    goal: str
    status: str
    priority: int
    yield_before: Optional[float] = None
    yield_after: Optional[float] = None


@dataclass
class Message:
    """NOP communication message."""
    id: str
    channel: str
    sender: str
    recipient: str
    text: str
    timestamp: int


@dataclass
class ToolDef:
    """Framework-agnostic tool definition."""
    name: str
    description: str
    parameters: dict
    handler: str


# Tool definitions for all 16 THUNDERFIRE tools
TOOLS = [
    ToolDef(
        name="thunderfire_node_list",
        description="List all connected THUNDERFIRE autonomous nodes with IDs, tiers, class types, and health status.",
        parameters={"type": "object", "properties": {}},
        handler="node_list"
    ),
    ToolDef(
        name="thunderfire_node_health",
        description="Get detailed CHITRAL health (7 fields: Capability, Health, Intent, Timeline, Resources, Authority, Lifecycle) for a specific node.",
        parameters={
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Node identifier"}
            },
            "required": ["node_id"]
        },
        handler="node_health"
    ),
    ToolDef(
        name="thunderfire_node_create",
        description="Create a new THUNDERFIRE node with the specified name, class type, and hardware tier.",
        parameters={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Node name"},
                "class_type": {"type": "string", "description": "Node class type (e.g., 'sensor', 'actuator', 'robot')"},
                "tier": {"type": "integer", "description": "Hardware tier (0-9)"}
            },
            "required": ["name", "class_type", "tier"]
        },
        handler="node_create"
    ),
    ToolDef(
        name="thunderfire_marketplace_search",
        description="Search the TF Store marketplace for modules and packages.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "category": {"type": "string", "description": "Filter by category"}
            },
            "required": ["query"]
        },
        handler="marketplace_search"
    ),
    ToolDef(
        name="thunderfire_marketplace_install",
        description="Install a package from TF Store onto a node.",
        parameters={
            "type": "object",
            "properties": {
                "package_name": {"type": "string", "description": "Package name to install"},
                "version": {"type": "string", "description": "Specific version (optional)"},
                "node_id": {"type": "string", "description": "Target node (optional, defaults to local)"}
            },
            "required": ["package_name"]
        },
        handler="marketplace_install"
    ),
    ToolDef(
        name="thunderfire_chitral_decode",
        description="Decode a CHITRAL hex message into structured fields.",
        parameters={
            "type": "object",
            "properties": {
                "hex": {"type": "string", "description": "CHITRAL hex string"}
            },
            "required": ["hex"]
        },
        handler="chitral_decode"
    ),
    ToolDef(
        name="thunderfire_chitral_status",
        description="Get CHITRAL status summary for a node.",
        parameters={
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Node identifier"}
            },
            "required": ["node_id"]
        },
        handler="chitral_status"
    ),
    ToolDef(
        name="thunderfire_theta_run",
        description="Execute a THETA decision cycle on a node.",
        parameters={
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Node identifier"},
                "stage": {"type": "integer", "description": "THETA stage (1-12, optional)"},
                "params": {"type": "object", "description": "Stage parameters"}
            },
            "required": ["node_id"]
        },
        handler="theta_run"
    ),
    ToolDef(
        name="thunderfire_theta_status",
        description="Get current THETA status for a node.",
        parameters={
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "Node identifier"}
            },
            "required": ["node_id"]
        },
        handler="theta_status"
    ),
    ToolDef(
        name="thunderfire_service_discover",
        description="Discover available NOP services in the network.",
        parameters={
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Filter by capability category"},
                "min_tier": {"type": "integer", "description": "Minimum tier requirement"}
            }
        },
        handler="service_discover"
    ),
    ToolDef(
        name="thunderfire_service_request",
        description="Request a NOP service and begin negotiation.",
        parameters={
            "type": "object",
            "properties": {
                "service_id": {"type": "string", "description": "Service identifier"},
                "params": {"type": "object", "description": "Request parameters"}
            },
            "required": ["service_id"]
        },
        handler="service_request"
    ),
    ToolDef(
        name="thunderfire_gym_tasks",
        description="List GYM autonomous improvement tasks.",
        parameters={"type": "object", "properties": {}},
        handler="gym_tasks"
    ),
    ToolDef(
        name="thunderfire_gym_complete",
        description="Mark a GYM task as completed with results.",
        parameters={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "Task identifier"},
                "result": {"type": "object", "description": "Task completion result"}
            },
            "required": ["task_id", "result"]
        },
        handler="gym_complete"
    ),
    ToolDef(
        name="thunderfire_msg_send",
        description="Send a message via NOP communication channel.",
        parameters={
            "type": "object",
            "properties": {
                "channel": {"type": "string", "description": "Channel (telegram, slack, discord, etc.)"},
                "recipient": {"type": "string", "description": "Recipient identifier"},
                "text": {"type": "string", "description": "Message text"}
            },
            "required": ["channel", "recipient", "text"]
        },
        handler="msg_send"
    ),
    ToolDef(
        name="thunderfire_msg_history",
        description="Get message history for a channel.",
        parameters={
            "type": "object",
            "properties": {
                "channel": {"type": "string", "description": "Channel name"},
                "limit": {"type": "integer", "description": "Max messages to return"}
            },
            "required": ["channel"]
        },
        handler="msg_history"
    ),
    ToolDef(
        name="thunderfire_script_eval",
        description="Execute a TOP Script on a node.",
        parameters={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "TOP Script code to execute"},
                "node_id": {"type": "string", "description": "Target node (optional)"}
            },
            "required": ["code"]
        },
        handler="script_eval"
    ),
]

# Map tool names to handler method names
TOOL_HANDLER_MAP = {tool.name: tool.handler for tool in TOOLS}
