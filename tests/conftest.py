"""
THUNDERFIRE Test Configuration

Shared fixtures and mock API for all tests.
"""

import pytest
import json
from typing import Any

# Mock responses for TOP API
MOCK_NODES = [
    {"id": "node-001", "name": "Sensor Alpha", "tier": 2, "class_type": 12, "health": 95, "status": "active"},
    {"id": "node-002", "name": "Robot Beta", "tier": 4, "class_type": 18, "health": 87, "status": "active"},
]

MOCK_NODE_HEALTH = {
    "capability": 100,
    "health": 95,
    "intent": 80,
    "timeline": 90,
    "resources": 75,
    "authority": 100,
    "lifecycle": 85,
    "uptime": 3600,
    "cpu": 45,
    "memory": 60,
    "errors": 0
}

MOCK_PACKAGES = [
    {"name": "nav-slam", "version": "2.1.0", "description": "SLAM navigation", "category": "navigation"},
    {"name": "vision-detect", "version": "1.5.0", "description": "Object detection", "category": "perception"},
]

MOCK_SERVICES = [
    {"id": "svc-001", "name": "Compute Service", "category": "compute", "tier": 3, "price": {"amount": 0.1, "unit": "hour"}},
]

MOCK_GYM_TASKS = [
    {"id": "GYM-001", "goal": "Reduce latency", "status": "OPEN", "priority": 1},
    {"id": "GYM-002", "goal": "Improve accuracy", "status": "IN_PROGRESS", "priority": 2},
]


class MockResponse:
    def __init__(self, data: Any, status_code: int = 200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def create_mock_rpc_handler():
    """Create a mock RPC handler that returns appropriate responses."""

    def handler(method: str, params: dict) -> dict:
        handlers = {
            "top.api.status": {"status": "ok", "version": "1.0.0"},
            "top.node.list": MOCK_NODES,
            "top.node.health": MOCK_NODE_HEALTH,
            "top.create_node": {"node_id": "node-new", "name": params.get("name", ""), "status": "created"},
            "top.marketplace.search": MOCK_PACKAGES,
            "top.marketplace.install": {"status": "installing", "package": params.get("name", "")},
            "top.chitral.decode": {"format": "CHITRAL-98", "fields": {"health": 95}},
            "top.theta.run": {"cycle_id": "cycle-001", "stage": params.get("stage", 1)},
            "top.theta.state": {"stage": "V0", "cycle_count": 5, "current_goal": "navigate"},
            "top.nop.services.search": MOCK_SERVICES,
            "top.nop.services.negotiate": {"negotiation_id": "neg-001", "status": "pending"},
            "top.gym.list": MOCK_GYM_TASKS,
            "top.gym.complete": {"status": "completed", "task_id": params.get("id", "")},
            "top.msg.send": {"status": "sent", "message_id": "msg-001"},
            "top.msg.conversations": [{"from": "user", "text": "Hello", "timestamp": 1234567890}],
            "top.script.eval": {"result": "success", "output": "Script executed"},
        }
        return {"result": handlers.get(method, {"error": "Unknown method"})}

    return handler


@pytest.fixture
def mock_rpc_handler():
    return create_mock_rpc_handler()


@pytest.fixture
def mock_api_url():
    return "http://mock-api:8080"


@pytest.fixture
def mock_api_key():
    return "tf_test_mock_key_12345678"
