#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest"]
# ///

"""Tests for parameter parsing functionality."""

import pytest

from midjargon.core.parameters import parse_parameters
from midjargon.core.parser import split_text_and_parameters


def test_basic_parameter_parsing():
    """Test parsing of basic parameters."""
    param_str = "--ar 16:9 --stylize 100"
    params = parse_parameters(param_str)
    assert params["ar"] == "16:9"
    assert params["stylize"] == "100"


def test_flag_parameters():
    """Test parsing of flag parameters (without values)."""
    param_str = "--tile --raw"
    params = parse_parameters(param_str)
    assert params["tile"] is None
    assert params["raw"] is None


def test_parameter_with_multiple_values():
    """Test parsing parameters that accept multiple values."""
    param_str = "--no blur,cars,watermark"
    params = parse_parameters(param_str)
    assert params["no"] == "blur,cars,watermark"


def test_parameter_with_spaces():
    """Test parsing parameters with values containing spaces."""
    param_str = '--style "raw photo" --seed 123456'
    params = parse_parameters(param_str)
    assert params["style"] == "raw photo"
    assert params["seed"] == "123456"


def test_mixed_parameters():
    """Test parsing a mix of different parameter types."""
    param_str = '--ar 16:9 --tile --no blur,cars --style "raw photo"'
    params = parse_parameters(param_str)
    assert params["ar"] == "16:9"
    assert params["tile"] is None
    assert params["no"] == "blur,cars"
    assert params["style"] == "raw photo"


def test_split_text_and_parameters():
    """Test splitting text from parameters."""
    prompt = 'a beautiful landscape --ar 16:9 --style "raw photo"'
    text, params = split_text_and_parameters(prompt)
    assert text == "a beautiful landscape"
    assert '--ar 16:9 --style "raw photo"' in params


def test_parameter_order():
    """Test that parameter order is preserved in output."""
    param_str = "--seed 123 --ar 16:9 --chaos 20 --tile"
    params = parse_parameters(param_str)
    keys = list(params.keys())
    assert keys == ["seed", "ar", "chaos", "tile"]


def test_invalid_parameters():
    """Test handling of invalid parameter formats."""
    with pytest.raises(ValueError):
        parse_parameters("--")  # Empty parameter name

    with pytest.raises(ValueError):
        parse_parameters("--ar")  # Missing required value

    with pytest.raises(ValueError):
        parse_parameters("ar 16:9")  # Missing -- prefix
