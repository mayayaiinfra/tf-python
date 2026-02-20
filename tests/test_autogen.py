"""
Tests for AutoGen integration
"""

import pytest


class TestAutoGenTools:
    """Tests for ThunderFireAutoGen."""

    def test_autogen_import(self):
        """AutoGen integration can be imported."""
        from thunderfire.autogen import ThunderFireAutoGen
        assert ThunderFireAutoGen is not None

    def test_autogen_init(self):
        """ThunderFireAutoGen initializes correctly."""
        from thunderfire.autogen import ThunderFireAutoGen

        tf = ThunderFireAutoGen(api_key="test")
        assert tf.client is not None

    def test_get_tool_functions_returns_16(self):
        """get_tool_functions returns 16 functions."""
        from thunderfire.autogen import ThunderFireAutoGen

        tf = ThunderFireAutoGen(api_key="test")
        funcs = tf.get_tool_functions()

        assert len(funcs) == 16

    def test_tool_functions_are_callable(self):
        """All tool functions are callable."""
        from thunderfire.autogen import ThunderFireAutoGen

        tf = ThunderFireAutoGen(api_key="test")
        funcs = tf.get_tool_functions()

        for name, func in funcs.items():
            assert callable(func), f"{name} is not callable"
