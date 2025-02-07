"""Tests for base engine functionality."""

import pytest
from pydantic import BaseModel

from midjargon.engines.base import EngineParser


class TestPrompt(BaseModel):
    """Test implementation of prompt model."""

    text: str
    parameters: dict[str, str | None]

    def to_string(self) -> str:
        """Convert prompt to string representation."""
        return f"{self.text} {' '.join(f'{k} {v}' if v else k for k, v in self.parameters.items())}"


class TestEngine(EngineParser[TestPrompt]):
    """Test implementation of engine parser."""

    def _parse_dict(self, midjargon_dict: dict) -> TestPrompt:
        """Parse dictionary into test prompt."""
        # Extract text and parameters
        text = midjargon_dict.get("text", "")
        parameters = {
            k: str(v) if v is not None else None
            for k, v in midjargon_dict.items()
            if k not in ["text", "images"]
        }
        return TestPrompt(text=text, parameters=parameters)

    def parse_dict(self, midjargon_dict: dict) -> TestPrompt:
        """Parse a dictionary into a TestPrompt object."""
        # Call super() to validate empty prompt
        super().parse_dict(midjargon_dict)
        return self._parse_dict(midjargon_dict)

    def to_dict(self, prompt: TestPrompt) -> dict:
        """Convert a TestPrompt back to a dictionary."""
        result: dict[str, str | None] = {"text": prompt.text}
        result.update(prompt.parameters)
        return result


def test_engine_parsing():
    """Test basic prompt parsing in engine."""
    engine = TestEngine()
    input_dict = {"text": "test prompt", "param1": "value1", "flag": None}
    result = engine.parse_dict(input_dict)
    assert isinstance(result, TestPrompt)
    assert result.text == "test prompt"
    assert result.parameters["param1"] == "value1"
    assert result.parameters["flag"] is None


def test_prompt_to_string():
    """Test prompt string conversion."""
    prompt = TestPrompt(text="test", parameters={"param": "value", "flag": None})
    assert prompt.to_string() == "test param value flag"


def test_engine_validation():
    """Test engine validation."""
    with pytest.raises(
        TypeError, match="Can't instantiate abstract class EngineParser"
    ):
        # Should fail because EngineParser is abstract
        EngineParser()


def test_engine_with_empty_prompt():
    """Test engine handling of empty prompt."""
    engine = TestEngine()
    with pytest.raises(ValueError, match="Empty prompt"):
        engine.parse_dict({"text": ""})


def test_engine_with_complex_prompt():
    """Test engine handling of complex prompt."""
    engine = TestEngine()
    input_dict = {
        "text": "test prompt",
        "param1": "value with spaces",
        "param2": "123",
        "flag": None,
    }
    result = engine.parse_dict(input_dict)
    assert result.text == "test prompt"
    assert result.parameters["param1"] == "value with spaces"
    assert result.parameters["param2"] == "123"
    assert result.parameters["flag"] is None


def test_engine_roundtrip():
    """Test conversion between dict and prompt formats."""
    engine = TestEngine()
    input_dict = {"text": "test prompt", "param1": "value1", "flag": None}
    prompt = engine.parse_dict(input_dict)
    output_dict = engine.to_dict(prompt)
    assert output_dict["text"] == input_dict["text"]
    assert output_dict["param1"] == input_dict["param1"]
    assert output_dict["flag"] == input_dict["flag"]


def test_engine_with_permutations():
    """Test engine handling of permutations."""
    engine = TestEngine()

    # Test with parameter permutations
    input_dicts = [
        {"text": "smooth edges", "stylize": "75"},
        {"text": "smooth edges", "stylize": "300"},
        {"text": "smooth edges", "stylize": "75", "personalization": None},
        {"text": "smooth edges", "stylize": "300", "personalization": None},
    ]

    results = [engine.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {
        (
            r.text.strip(),
            r.parameters.get("stylize"),
            r.parameters.get("personalization"),
        )
        for r in results
    }

    expected = {
        ("smooth edges", "75", None),
        ("smooth edges", "300", None),
        ("smooth edges", "75", None),
        ("smooth edges", "300", None),
    }

    assert result_tuples == expected

    # Test with flag permutations
    input_dicts = [
        {"text": "photo"},
        {"text": "photo", "tile": None},
        {"text": "photo", "turbo": None},
        {"text": "photo", "tile": None, "turbo": None},
    ]

    results = [engine.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {
        (r.text.strip(), "tile" in r.parameters, "turbo" in r.parameters)
        for r in results
    }

    expected = {
        ("photo", False, False),
        ("photo", True, False),
        ("photo", False, True),
        ("photo", True, True),
    }

    assert result_tuples == expected
