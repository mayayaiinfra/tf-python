"""
Tests for CrewAI integration
"""

import pytest


class TestCrewAITools:
    """Tests for ThunderFireTools."""

    def test_tools_import(self):
        """Tools can be imported."""
        try:
            from thunderfire.crewai import ThunderFireTools
            assert ThunderFireTools is not None
        except ImportError as e:
            if "crewai" in str(e):
                pytest.skip("CrewAI not installed")
            raise

    def test_tools_returns_16_functions(self):
        """get_tools returns 16 tools."""
        try:
            from thunderfire.crewai import ThunderFireTools
        except ImportError:
            pytest.skip("CrewAI not installed")

        tf = ThunderFireTools(api_key="test")
        tools = tf.get_tools()

        assert len(tools) == 16

    def test_tools_are_callable(self):
        """All tools are callable."""
        try:
            from thunderfire.crewai import ThunderFireTools
        except ImportError:
            pytest.skip("CrewAI not installed")

        tf = ThunderFireTools(api_key="test")
        tools = tf.get_tools()

        for tool in tools:
            assert callable(tool)

    def test_client_accessible(self):
        """Client is accessible for testing."""
        try:
            from thunderfire.crewai import ThunderFireTools
        except ImportError:
            pytest.skip("CrewAI not installed")

        tf = ThunderFireTools(api_key="test")
        assert tf._client is not None
