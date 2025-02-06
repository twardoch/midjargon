#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest"]
# ///

"""Tests for base engine functionality."""

import pytest

from midjargon.engines.base import BaseEngine, BasePrompt


class TestPrompt(BasePrompt):
    """Test implementation of BasePrompt."""

    def __init__(self, text: str, parameters: dict[str, str | None]):
        self.text = text
        self.parameters = parameters

    def to_string(self) -> str:
        return f"{self.text} {' '.join(f'{k} {v}' if v else k for k, v in self.parameters.items())}"


class TestEngine(BaseEngine[TestPrompt]):
    """Test implementation of BaseEngine."""

    def parse_prompt(self, input_str: str) -> TestPrompt:
        text, *params = input_str.split("--")
        parameters = {}
        for param in params:
            parts = param.strip().split(maxsplit=1)
            if len(parts) == 1:
                parameters[f"--{parts[0]}"] = None
            else:
                parameters[f"--{parts[0]}"] = parts[1]
        return TestPrompt(text.strip(), parameters)


def test_base_engine_parsing():
    """Test basic prompt parsing in base engine."""
    engine = TestEngine()
    result = engine.parse_prompt("test prompt --param1 value1 --flag")
    assert isinstance(result, TestPrompt)
    assert result.text == "test prompt"
    assert result.parameters["--param1"] == "value1"
    assert result.parameters["--flag"] is None


def test_base_prompt_to_string():
    """Test prompt string conversion."""
    prompt = TestPrompt("test", {"--param": "value", "--flag": None})
    assert prompt.to_string() == "test --param value --flag"


def test_base_engine_validation():
    """Test base engine validation."""
    with pytest.raises(TypeError):
        # Should fail because BaseEngine is abstract
        BaseEngine()


def test_base_prompt_validation():
    """Test base prompt validation."""
    with pytest.raises(TypeError):
        # Should fail because BasePrompt is abstract
        BasePrompt()


def test_engine_with_empty_prompt():
    """Test engine handling of empty prompt."""
    engine = TestEngine()
    with pytest.raises(ValueError):
        engine.parse_prompt("")
    with pytest.raises(ValueError):
        engine.parse_prompt("   ")


def test_engine_with_complex_prompt():
    """Test engine handling of complex prompt."""
    engine = TestEngine()
    result = engine.parse_prompt(
        'test prompt --param1 "value with spaces" --param2 123 --flag'
    )
    assert result.text == "test prompt"
    assert result.parameters["--param1"] == '"value with spaces"'
    assert result.parameters["--param2"] == "123"
    assert result.parameters["--flag"] is None
