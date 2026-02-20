"""
THUNDERFIRE LangChain Toolkit

Provides 16 tools as LangChain BaseTool subclasses.
"""

import json
from typing import Optional, Any, Type

from ..client import ThunderFireClient, ThunderFireClientSync

try:
    from langchain_core.tools import BaseTool
    from pydantic import BaseModel, Field
except ImportError:
    raise ImportError(
        "LangChain integration requires langchain-core. "
        "Install with: pip install thunderfire[langchain]"
    )


class ThunderFireToolkit:
    """LangChain toolkit for THUNDERFIRE autonomous node management."""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.client = ThunderFireClient(api_url, api_key)
        self.sync_client = ThunderFireClientSync(api_url, api_key)

    def get_tools(self) -> list[BaseTool]:
        """Return all 16 tools as LangChain BaseTool instances."""
        return [
            NodeListTool(client=self.client, sync_client=self.sync_client),
            NodeHealthTool(client=self.client, sync_client=self.sync_client),
            NodeCreateTool(client=self.client, sync_client=self.sync_client),
            MarketplaceSearchTool(client=self.client, sync_client=self.sync_client),
            MarketplaceInstallTool(client=self.client, sync_client=self.sync_client),
            ChitralDecodeTool(client=self.client, sync_client=self.sync_client),
            ChitralStatusTool(client=self.client, sync_client=self.sync_client),
            ThetaRunTool(client=self.client, sync_client=self.sync_client),
            ThetaStatusTool(client=self.client, sync_client=self.sync_client),
            ServiceDiscoverTool(client=self.client, sync_client=self.sync_client),
            ServiceRequestTool(client=self.client, sync_client=self.sync_client),
            GymTasksTool(client=self.client, sync_client=self.sync_client),
            GymCompleteTool(client=self.client, sync_client=self.sync_client),
            MsgSendTool(client=self.client, sync_client=self.sync_client),
            MsgHistoryTool(client=self.client, sync_client=self.sync_client),
            ScriptEvalTool(client=self.client, sync_client=self.sync_client),
        ]


# Tool input models
class NodeIdInput(BaseModel):
    node_id: str = Field(description="Node identifier")


class NodeCreateInput(BaseModel):
    name: str = Field(description="Node name")
    class_type: str = Field(description="Node class type")
    tier: int = Field(description="Hardware tier (0-9)")


class MarketplaceSearchInput(BaseModel):
    query: str = Field(description="Search query")
    category: Optional[str] = Field(default=None, description="Filter by category")


class MarketplaceInstallInput(BaseModel):
    package_name: str = Field(description="Package name to install")
    version: Optional[str] = Field(default=None, description="Specific version")
    node_id: Optional[str] = Field(default=None, description="Target node")


class ChitralDecodeInput(BaseModel):
    hex: str = Field(description="CHITRAL hex string")


class ThetaRunInput(BaseModel):
    node_id: str = Field(description="Node identifier")
    stage: Optional[int] = Field(default=None, description="THETA stage (1-12)")
    params: Optional[dict] = Field(default=None, description="Stage parameters")


class ServiceDiscoverInput(BaseModel):
    category: Optional[str] = Field(default=None, description="Capability category")
    min_tier: Optional[int] = Field(default=None, description="Minimum tier")


class ServiceRequestInput(BaseModel):
    service_id: str = Field(description="Service identifier")
    params: Optional[dict] = Field(default=None, description="Request parameters")


class GymCompleteInput(BaseModel):
    task_id: str = Field(description="Task identifier")
    result: dict = Field(description="Task completion result")


class MsgSendInput(BaseModel):
    channel: str = Field(description="Channel (telegram, slack, etc.)")
    recipient: str = Field(description="Recipient identifier")
    text: str = Field(description="Message text")


class MsgHistoryInput(BaseModel):
    channel: str = Field(description="Channel name")
    limit: int = Field(default=20, description="Max messages")


class ScriptEvalInput(BaseModel):
    code: str = Field(description="TOP Script code")
    node_id: Optional[str] = Field(default=None, description="Target node")


# Tool implementations
class NodeListTool(BaseTool):
    name: str = "thunderfire_node_list"
    description: str = "List all connected THUNDERFIRE autonomous nodes with IDs, tiers, class types, and health status."
    client: Any = None
    sync_client: Any = None

    def _run(self) -> str:
        return json.dumps(self.sync_client.node_list())

    async def _arun(self) -> str:
        return json.dumps(await self.client.node_list())


class NodeHealthTool(BaseTool):
    name: str = "thunderfire_node_health"
    description: str = "Get detailed CHITRAL health (7 fields) for a specific node."
    args_schema: Type[BaseModel] = NodeIdInput
    client: Any = None
    sync_client: Any = None

    def _run(self, node_id: str) -> str:
        return json.dumps(self.sync_client.node_health(node_id))

    async def _arun(self, node_id: str) -> str:
        return json.dumps(await self.client.node_health(node_id))


class NodeCreateTool(BaseTool):
    name: str = "thunderfire_node_create"
    description: str = "Create a new THUNDERFIRE node with the specified name, class type, and tier."
    args_schema: Type[BaseModel] = NodeCreateInput
    client: Any = None
    sync_client: Any = None

    def _run(self, name: str, class_type: str, tier: int) -> str:
        return json.dumps(self.sync_client.node_create(name, class_type, tier))

    async def _arun(self, name: str, class_type: str, tier: int) -> str:
        return json.dumps(await self.client.node_create(name, class_type, tier))


class MarketplaceSearchTool(BaseTool):
    name: str = "thunderfire_marketplace_search"
    description: str = "Search the TF Store marketplace for modules and packages."
    args_schema: Type[BaseModel] = MarketplaceSearchInput
    client: Any = None
    sync_client: Any = None

    def _run(self, query: str, category: Optional[str] = None) -> str:
        return json.dumps(self.sync_client.marketplace_search(query, category))

    async def _arun(self, query: str, category: Optional[str] = None) -> str:
        return json.dumps(await self.client.marketplace_search(query, category))


class MarketplaceInstallTool(BaseTool):
    name: str = "thunderfire_marketplace_install"
    description: str = "Install a package from TF Store onto a node."
    args_schema: Type[BaseModel] = MarketplaceInstallInput
    client: Any = None
    sync_client: Any = None

    def _run(self, package_name: str, version: Optional[str] = None, node_id: Optional[str] = None) -> str:
        return json.dumps(self.sync_client.marketplace_install(package_name, version, node_id))

    async def _arun(self, package_name: str, version: Optional[str] = None, node_id: Optional[str] = None) -> str:
        return json.dumps(await self.client.marketplace_install(package_name, version, node_id))


class ChitralDecodeTool(BaseTool):
    name: str = "thunderfire_chitral_decode"
    description: str = "Decode a CHITRAL hex message into structured fields."
    args_schema: Type[BaseModel] = ChitralDecodeInput
    client: Any = None
    sync_client: Any = None

    def _run(self, hex: str) -> str:
        return json.dumps(self.sync_client.chitral_decode(hex))

    async def _arun(self, hex: str) -> str:
        return json.dumps(await self.client.chitral_decode(hex))


class ChitralStatusTool(BaseTool):
    name: str = "thunderfire_chitral_status"
    description: str = "Get CHITRAL status summary for a node."
    args_schema: Type[BaseModel] = NodeIdInput
    client: Any = None
    sync_client: Any = None

    def _run(self, node_id: str) -> str:
        return json.dumps(self.sync_client.chitral_status(node_id))

    async def _arun(self, node_id: str) -> str:
        return json.dumps(await self.client.chitral_status(node_id))


class ThetaRunTool(BaseTool):
    name: str = "thunderfire_theta_run"
    description: str = "Execute a THETA decision cycle on a node."
    args_schema: Type[BaseModel] = ThetaRunInput
    client: Any = None
    sync_client: Any = None

    def _run(self, node_id: str, stage: Optional[int] = None, params: Optional[dict] = None) -> str:
        return json.dumps(self.sync_client.theta_run(node_id, stage, params))

    async def _arun(self, node_id: str, stage: Optional[int] = None, params: Optional[dict] = None) -> str:
        return json.dumps(await self.client.theta_run(node_id, stage, params))


class ThetaStatusTool(BaseTool):
    name: str = "thunderfire_theta_status"
    description: str = "Get current THETA status for a node."
    args_schema: Type[BaseModel] = NodeIdInput
    client: Any = None
    sync_client: Any = None

    def _run(self, node_id: str) -> str:
        return json.dumps(self.sync_client.theta_status(node_id))

    async def _arun(self, node_id: str) -> str:
        return json.dumps(await self.client.theta_status(node_id))


class ServiceDiscoverTool(BaseTool):
    name: str = "thunderfire_service_discover"
    description: str = "Discover available NOP services in the network."
    args_schema: Type[BaseModel] = ServiceDiscoverInput
    client: Any = None
    sync_client: Any = None

    def _run(self, category: Optional[str] = None, min_tier: Optional[int] = None) -> str:
        return json.dumps(self.sync_client.service_discover(category, min_tier))

    async def _arun(self, category: Optional[str] = None, min_tier: Optional[int] = None) -> str:
        return json.dumps(await self.client.service_discover(category, min_tier))


class ServiceRequestTool(BaseTool):
    name: str = "thunderfire_service_request"
    description: str = "Request a NOP service and begin negotiation."
    args_schema: Type[BaseModel] = ServiceRequestInput
    client: Any = None
    sync_client: Any = None

    def _run(self, service_id: str, params: Optional[dict] = None) -> str:
        return json.dumps(self.sync_client.service_request(service_id, params))

    async def _arun(self, service_id: str, params: Optional[dict] = None) -> str:
        return json.dumps(await self.client.service_request(service_id, params))


class GymTasksTool(BaseTool):
    name: str = "thunderfire_gym_tasks"
    description: str = "List GYM autonomous improvement tasks."
    client: Any = None
    sync_client: Any = None

    def _run(self) -> str:
        return json.dumps(self.sync_client.gym_tasks())

    async def _arun(self) -> str:
        return json.dumps(await self.client.gym_tasks())


class GymCompleteTool(BaseTool):
    name: str = "thunderfire_gym_complete"
    description: str = "Mark a GYM task as completed with results."
    args_schema: Type[BaseModel] = GymCompleteInput
    client: Any = None
    sync_client: Any = None

    def _run(self, task_id: str, result: dict) -> str:
        return json.dumps(self.sync_client.gym_complete(task_id, result))

    async def _arun(self, task_id: str, result: dict) -> str:
        return json.dumps(await self.client.gym_complete(task_id, result))


class MsgSendTool(BaseTool):
    name: str = "thunderfire_msg_send"
    description: str = "Send a message via NOP communication channel."
    args_schema: Type[BaseModel] = MsgSendInput
    client: Any = None
    sync_client: Any = None

    def _run(self, channel: str, recipient: str, text: str) -> str:
        return json.dumps(self.sync_client.msg_send(channel, recipient, text))

    async def _arun(self, channel: str, recipient: str, text: str) -> str:
        return json.dumps(await self.client.msg_send(channel, recipient, text))


class MsgHistoryTool(BaseTool):
    name: str = "thunderfire_msg_history"
    description: str = "Get message history for a channel."
    args_schema: Type[BaseModel] = MsgHistoryInput
    client: Any = None
    sync_client: Any = None

    def _run(self, channel: str, limit: int = 20) -> str:
        return json.dumps(self.sync_client.msg_history(channel, limit))

    async def _arun(self, channel: str, limit: int = 20) -> str:
        return json.dumps(await self.client.msg_history(channel, limit))


class ScriptEvalTool(BaseTool):
    name: str = "thunderfire_script_eval"
    description: str = "Execute a TOP Script on a node."
    args_schema: Type[BaseModel] = ScriptEvalInput
    client: Any = None
    sync_client: Any = None

    def _run(self, code: str, node_id: Optional[str] = None) -> str:
        return json.dumps(self.sync_client.script_eval(code, node_id))

    async def _arun(self, code: str, node_id: Optional[str] = None) -> str:
        return json.dumps(await self.client.script_eval(code, node_id))
