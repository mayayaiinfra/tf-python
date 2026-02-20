"""
Tests for ThunderFireClient
"""

import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch

from thunderfire.client import ThunderFireClient, ThunderFireClientSync


class TestThunderFireClient:
    """Tests for async client."""

    @pytest.mark.asyncio
    async def test_client_init_with_args(self):
        """Client initializes with provided arguments."""
        client = ThunderFireClient(
            api_url="http://test:8080",
            api_key="tf_test_key"
        )
        assert client.api_url == "http://test:8080"
        assert client.api_key == "tf_test_key"

    @pytest.mark.asyncio
    async def test_client_init_strips_trailing_slash(self):
        """Client removes trailing slash from URL."""
        client = ThunderFireClient(api_url="http://test:8080/")
        assert client.api_url == "http://test:8080"

    @pytest.mark.asyncio
    async def test_node_list_request(self, mock_rpc_handler):
        """node_list makes correct RPC call."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.node.list", {})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.node_list()
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_node_health_request(self, mock_rpc_handler):
        """node_health passes node_id correctly."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.node.health", {"id": "node-001"})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.node_health("node-001")
            assert "health" in result
            assert result["health"] == 95

    @pytest.mark.asyncio
    async def test_marketplace_search(self, mock_rpc_handler):
        """marketplace_search returns packages."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.marketplace.search", {"query": "nav"})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.marketplace_search("nav")
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_theta_run(self, mock_rpc_handler):
        """theta_run executes cycle."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.theta.run", {"id": "node-001"})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.theta_run("node-001")
            assert "cycle_id" in result

    @pytest.mark.asyncio
    async def test_gym_tasks(self, mock_rpc_handler):
        """gym_tasks returns task list."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.gym.list", {})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.gym_tasks()
            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_msg_send(self, mock_rpc_handler):
        """msg_send sends message."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.msg.send", {})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.msg_send("slack", "user-1", "Hello")
            assert result["status"] == "sent"

    @pytest.mark.asyncio
    async def test_script_eval(self, mock_rpc_handler):
        """script_eval executes script."""
        client = ThunderFireClient(api_key="test")

        with patch.object(client._client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_rpc_handler("top.script.eval", {})
            mock_post.return_value.raise_for_status = MagicMock()

            result = await client.script_eval("print('hello')")
            assert result["result"] == "success"


class TestThunderFireClientSync:
    """Tests for sync client wrapper."""

    def test_sync_client_init(self):
        """Sync client initializes correctly."""
        client = ThunderFireClientSync(api_key="test")
        assert client._async_client is not None

    def test_sync_wrapper_methods_exist(self):
        """Sync client has all expected methods."""
        client = ThunderFireClientSync(api_key="test")

        methods = [
            "node_list", "node_health", "node_create",
            "marketplace_search", "marketplace_install",
            "chitral_decode", "chitral_status",
            "theta_run", "theta_status",
            "service_discover", "service_request",
            "gym_tasks", "gym_complete",
            "msg_send", "msg_history",
            "script_eval"
        ]

        for method in methods:
            assert hasattr(client, method), f"Missing method: {method}"
