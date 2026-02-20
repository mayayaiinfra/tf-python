"""
Tests for OpenAI integration
"""

import pytest
import json


class TestOpenAIFunctions:
    """Tests for OpenAI function definitions."""

    def test_functions_import(self):
        """Functions can be imported."""
        from thunderfire.openai import get_function_definitions, handle_tool_call
        assert get_function_definitions is not None
        assert handle_tool_call is not None

    def test_returns_16_functions(self):
        """get_function_definitions returns 16 function definitions."""
        from thunderfire.openai import get_function_definitions

        funcs = get_function_definitions()
        assert len(funcs) == 16

    def test_function_format_correct(self):
        """Each function has correct OpenAI format."""
        from thunderfire.openai import get_function_definitions

        funcs = get_function_definitions()

        for func in funcs:
            assert func["type"] == "function"
            assert "function" in func
            assert "name" in func["function"]
            assert "description" in func["function"]
            assert "parameters" in func["function"]

    def test_parameters_are_json_schema(self):
        """Parameters are valid JSON Schema."""
        from thunderfire.openai import get_function_definitions

        funcs = get_function_definitions()

        for func in funcs:
            params = func["function"]["parameters"]
            assert params["type"] == "object"
            assert "properties" in params
