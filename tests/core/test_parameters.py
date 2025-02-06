#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest"]
# ///

"""Tests for parameter parsing functionality."""

import pytest

from midjargon.core.parameters import parse_parameters


def test_basic_parameter_parsing():
    """Test parsing of basic parameters."""
    param_str = "--ar 16:9 --stylize 100"
    params = parse_parameters(param_str)
    assert params["ar"] == "16:9"
    assert params["stylize"] == "100"


def test_flag_parameters():
    """Test parsing of flag parameters (without values)."""
    param_str = "--tile --turbo --relax"
    params = parse_parameters(param_str)
    assert params["tile"] is None
    assert params["turbo"] is None
    assert params["relax"] is None


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


def test_shorthand_parameters():
    """Test parsing of shorthand parameter names."""
    param_str = "--s 100 --c 50 --w 1000 --iw 2.0 --q 1.0"
    params = parse_parameters(param_str)
    assert params["stylize"] == "100"
    assert params["chaos"] == "50"
    assert params["weird"] == "1000"
    assert params["image_weight"] == "2.0"
    assert params["quality"] == "1.0"


def test_niji_version_parameter():
    """Test parsing of niji version parameter."""
    # Test basic niji
    params = parse_parameters("--niji")
    assert params["version"] == "niji"

    # Test niji with version
    params = parse_parameters("--niji 6")
    assert params["version"] == "niji 6"


def test_version_parameter():
    """Test parsing of version parameter."""
    # Test v parameter
    params = parse_parameters("--v 5.2")
    assert params["version"] == "5.2"


def test_personalization_parameter():
    """Test parsing of personalization parameter."""
    # Test basic p parameter
    params = parse_parameters("--p")
    assert params["personalization"] == ""

    # Test p with value
    params = parse_parameters("--p abc123")
    assert params["personalization"] == "abc123"


def test_reference_parameters():
    """Test parsing of reference parameters."""
    param_str = "--cref img1.jpg --sref style1.jpg,style2.jpg"
    params = parse_parameters(param_str)
    assert params["character_reference"] == "img1.jpg"
    assert params["style_reference"] == "style1.jpg,style2.jpg"


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

    with pytest.raises(ValueError):
        parse_parameters("--v")  # Missing version value

    with pytest.raises(ValueError):
        parse_parameters("--style invalid")  # Invalid style value
