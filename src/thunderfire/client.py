"""
THUNDERFIRE TOP API Client

Thin REST client for TOP Public API.
"""

import os
import asyncio
from typing import Any, Optional

import httpx


class ThunderFireClient:
    """Async client for TOP Public API."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0
    ):
        """
        Initialize THUNDERFIRE client.

        Args:
            api_url: TOP API URL (default: THUNDERFIRE_API_URL env or localhost:8080)
            api_key: API key (default: THUNDERFIRE_API_KEY env)
            timeout: Request timeout in seconds
        """
        self.api_url = (api_url or os.environ.get("THUNDERFIRE_API_URL", "http://localhost:8080")).rstrip("/")
        self.api_key = api_key or os.environ.get("THUNDERFIRE_API_KEY", "")
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def _request(self, method: str, params: Optional[dict] = None) -> Any:
        """Make JSON-RPC request to TOP API."""
        url = f"{self.api_url}/api/v1/rpc"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = await self._client.post(
            url,
            headers=headers,
            json={"method": method, "params": params or {}}
        )
        response.raise_for_status()

        data = response.json()
        if "error" in data:
            raise RuntimeError(data["error"].get("message", "RPC error"))

        return data.get("result")

    async def validate(self) -> bool:
        """Validate API connection."""
        try:
            await self._request("top.api.status")
            return True
        except Exception:
            return False

    # Node operations
    async def node_list(self) -> list[dict]:
        """List all connected nodes."""
        return await self._request("top.node.list")

    async def node_health(self, node_id: str) -> dict:
        """Get CHITRAL health for a node."""
        return await self._request("top.node.health", {"id": node_id})

    async def node_create(self, name: str, class_type: str, tier: int) -> dict:
        """Create a new node."""
        return await self._request("top.create_node", {
            "name": name, "class_type": class_type, "tier": tier
        })

    # Marketplace
    async def marketplace_search(self, query: str, category: Optional[str] = None) -> list[dict]:
        """Search TF Store packages."""
        return await self._request("top.marketplace.search", {
            "query": query, "category": category
        })

    async def marketplace_install(
        self,
        package_name: str,
        version: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> dict:
        """Install a package from TF Store."""
        return await self._request("top.marketplace.install", {
            "name": package_name, "version": version, "node_id": node_id
        })

    # CHITRAL
    async def chitral_decode(self, hex_str: str) -> dict:
        """Decode CHITRAL hex message."""
        return await self._request("top.chitral.decode", {"msg": hex_str})

    async def chitral_status(self, node_id: str) -> dict:
        """Get CHITRAL status for a node."""
        return await self._request("top.node.health", {"id": node_id})

    # THETA
    async def theta_run(
        self,
        node_id: str,
        stage: Optional[int] = None,
        params: Optional[dict] = None
    ) -> dict:
        """Execute THETA cycle on a node."""
        return await self._request("top.theta.run", {
            "id": node_id, "stage": stage, "params": params
        })

    async def theta_status(self, node_id: str) -> dict:
        """Get THETA status for a node."""
        return await self._request("top.theta.state", {"id": node_id})

    # Services
    async def service_discover(
        self,
        category: Optional[str] = None,
        min_tier: Optional[int] = None
    ) -> list[dict]:
        """Discover NOP services."""
        return await self._request("top.nop.services.search", {
            "capability": category, "tier": min_tier
        })

    async def service_request(self, service_id: str, params: Optional[dict] = None) -> dict:
        """Request a NOP service."""
        return await self._request("top.nop.services.negotiate", {
            "service_id": service_id, "requirements": params or {}
        })

    # GYM
    async def gym_tasks(self) -> list[dict]:
        """List GYM tasks."""
        return await self._request("top.gym.list")

    async def gym_complete(self, task_id: str, result: dict) -> dict:
        """Complete a GYM task."""
        return await self._request("top.gym.complete", {"id": task_id, "result": result})

    # Messaging
    async def msg_send(self, channel: str, recipient: str, text: str) -> dict:
        """Send a message via NOP."""
        return await self._request("top.msg.send", {
            "to": recipient, "message": text, "channel": channel
        })

    async def msg_history(self, channel: str, limit: int = 20) -> list[dict]:
        """Get message history."""
        return await self._request("top.msg.conversations", {
            "channel": channel, "limit": limit
        })

    # Script
    async def script_eval(self, code: str, node_id: Optional[str] = None) -> dict:
        """Execute TOP Script."""
        return await self._request("top.script.eval", {
            "code": code, "node_id": node_id
        })

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()


class ThunderFireClientSync:
    """Synchronous wrapper for ThunderFireClient."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0
    ):
        self._async_client = ThunderFireClient(api_url, api_key, timeout)

    def _run(self, coro):
        """Run async coroutine synchronously."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

    def validate(self) -> bool:
        return self._run(self._async_client.validate())

    def node_list(self) -> list[dict]:
        return self._run(self._async_client.node_list())

    def node_health(self, node_id: str) -> dict:
        return self._run(self._async_client.node_health(node_id))

    def node_create(self, name: str, class_type: str, tier: int) -> dict:
        return self._run(self._async_client.node_create(name, class_type, tier))

    def marketplace_search(self, query: str, category: Optional[str] = None) -> list[dict]:
        return self._run(self._async_client.marketplace_search(query, category))

    def marketplace_install(
        self,
        package_name: str,
        version: Optional[str] = None,
        node_id: Optional[str] = None
    ) -> dict:
        return self._run(self._async_client.marketplace_install(package_name, version, node_id))

    def chitral_decode(self, hex_str: str) -> dict:
        return self._run(self._async_client.chitral_decode(hex_str))

    def chitral_status(self, node_id: str) -> dict:
        return self._run(self._async_client.chitral_status(node_id))

    def theta_run(
        self,
        node_id: str,
        stage: Optional[int] = None,
        params: Optional[dict] = None
    ) -> dict:
        return self._run(self._async_client.theta_run(node_id, stage, params))

    def theta_status(self, node_id: str) -> dict:
        return self._run(self._async_client.theta_status(node_id))

    def service_discover(
        self,
        category: Optional[str] = None,
        min_tier: Optional[int] = None
    ) -> list[dict]:
        return self._run(self._async_client.service_discover(category, min_tier))

    def service_request(self, service_id: str, params: Optional[dict] = None) -> dict:
        return self._run(self._async_client.service_request(service_id, params))

    def gym_tasks(self) -> list[dict]:
        return self._run(self._async_client.gym_tasks())

    def gym_complete(self, task_id: str, result: dict) -> dict:
        return self._run(self._async_client.gym_complete(task_id, result))

    def msg_send(self, channel: str, recipient: str, text: str) -> dict:
        return self._run(self._async_client.msg_send(channel, recipient, text))

    def msg_history(self, channel: str, limit: int = 20) -> list[dict]:
        return self._run(self._async_client.msg_history(channel, limit))

    def script_eval(self, code: str, node_id: Optional[str] = None) -> dict:
        return self._run(self._async_client.script_eval(code, node_id))

    def close(self):
        self._run(self._async_client.close())
