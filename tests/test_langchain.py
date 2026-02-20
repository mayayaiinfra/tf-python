"""
Tests for LangChain integration
"""

import pytest
from unittest.mock import MagicMock, patch


class TestLangChainToolkit:
    """Tests for ThunderFireToolkit."""

    def test_toolkit_import(self):
        """Toolkit can be imported."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
            assert ThunderFireToolkit is not None
        except ImportError as e:
            if "langchain" in str(e):
                pytest.skip("LangChain not installed")
            raise

    def test_toolkit_returns_16_tools(self):
        """Toolkit returns all 16 tools."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
        except ImportError:
            pytest.skip("LangChain not installed")

        toolkit = ThunderFireToolkit(api_key="test")
        tools = toolkit.get_tools()

        assert len(tools) == 16

    def test_tools_have_correct_names(self):
        """Each tool has the expected name."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
        except ImportError:
            pytest.skip("LangChain not installed")

        toolkit = ThunderFireToolkit(api_key="test")
        tools = toolkit.get_tools()

        expected_names = [
            "thunderfire_node_list",
            "thunderfire_node_health",
            "thunderfire_node_create",
            "thunderfire_marketplace_search",
            "thunderfire_marketplace_install",
            "thunderfire_chitral_decode",
            "thunderfire_chitral_status",
            "thunderfire_theta_run",
            "thunderfire_theta_status",
            "thunderfire_service_discover",
            "thunderfire_service_request",
            "thunderfire_gym_tasks",
            "thunderfire_gym_complete",
            "thunderfire_msg_send",
            "thunderfire_msg_history",
            "thunderfire_script_eval",
        ]

        tool_names = [t.name for t in tools]
        for name in expected_names:
            assert name in tool_names, f"Missing tool: {name}"

    def test_tools_have_descriptions(self):
        """Each tool has a non-empty description."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
        except ImportError:
            pytest.skip("LangChain not installed")

        toolkit = ThunderFireToolkit(api_key="test")
        tools = toolkit.get_tools()

        for tool in tools:
            assert tool.description, f"Tool {tool.name} has no description"
            assert len(tool.description) > 10

    def test_tool_has_run_method(self):
        """Tools have _run method."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
        except ImportError:
            pytest.skip("LangChain not installed")

        toolkit = ThunderFireToolkit(api_key="test")
        tools = toolkit.get_tools()

        for tool in tools:
            assert hasattr(tool, "_run"), f"Tool {tool.name} missing _run"
            assert hasattr(tool, "_arun"), f"Tool {tool.name} missing _arun"

    def test_tool_has_async_run_method(self):
        """Tools have _arun method for async execution."""
        try:
            from thunderfire.langchain import ThunderFireToolkit
        except ImportError:
            pytest.skip("LangChain not installed")

        toolkit = ThunderFireToolkit(api_key="test")
        tools = toolkit.get_tools()

        for tool in tools:
            assert hasattr(tool, "_arun")
            assert callable(tool._arun)
