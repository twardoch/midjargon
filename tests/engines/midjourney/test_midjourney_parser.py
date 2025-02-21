# this_file: tests/engines/midjourney/test_midjourney_parser.py
"""Tests for Midjourney parser."""

import pytest
from pydantic import HttpUrl

from midjargon.engines.midjourney import MidjourneyParser

# Test constants
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
WEIRD_VALUE = 1000
SEED_VALUE = 12345
STOP_VALUE = 80
IMAGE_WEIGHT_VALUE = 2.0
VERSION_NUMBER = "5.2"
DEFAULT_STYLIZE = 100
QUALITY_VALUE = 1.5
CHARACTER_WEIGHT_VALUE = 50
STYLE_WEIGHT_VALUE = 500
STYLE_VERSION_VALUE = 3
REPEAT_VALUE = 5


def test_numeric_parameters():
    """Test parsing of numeric parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "stylize": str(STYLIZE_VALUE),
            "seed": str(SEED_VALUE),
            "chaos": str(CHAOS_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.stylize == float(STYLIZE_VALUE)
    assert prompt.seed == SEED_VALUE
    assert prompt.chaos == float(CHAOS_VALUE)


def test_style_parameters():
    """Test parsing of style parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {"text": "a photo", "style": "raw", "version": VERSION_NUMBER}
    )

    assert prompt.text == "a photo"
    assert prompt.style == "raw"
    assert prompt.version == f"v{VERSION_NUMBER}"


def test_aspect_ratio():
    """Test parsing of aspect ratio."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict({"text": "a photo", "ar": "16:9"})

    assert prompt.text == "a photo"
    assert prompt.aspect_width == 16
    assert prompt.aspect_height == 9
    assert prompt.aspect_ratio == "16:9"


def test_image_prompts():
    """Test parsing of image prompts."""
    parser = MidjourneyParser()
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = parser.parse_dict({"text": "a fusion", "image_prompts": urls})

    assert prompt.text == "a fusion"
    assert len(prompt.image_prompts) == 2
    assert all(isinstance(url, HttpUrl) for url in prompt.image_prompts)
    assert [str(url) for url in prompt.image_prompts] == urls


def test_extra_parameters():
    """Test handling of unknown parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "unknown": "value",
            "flag": None,
        }
    )

    assert prompt.text == "a photo"
    assert prompt.extra_params == {"unknown": "value", "flag": None}


def test_parameter_conversion():
    """Test parameter value conversion."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "stylize": str(STYLIZE_VALUE),
            "seed": str(SEED_VALUE),
            "image_weight": str(IMAGE_WEIGHT_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.stylize == float(STYLIZE_VALUE)
    assert prompt.seed == SEED_VALUE
    assert prompt.image_weight == float(IMAGE_WEIGHT_VALUE)


def test_invalid_values():
    """Test handling of invalid parameter values."""
    parser = MidjourneyParser()

    # Invalid aspect ratio - now accepts any value
    result = parser.parse_dict({"text": "a photo", "ar": "999:999"})
    assert result.aspect_width == 999
    assert result.aspect_height == 999
    assert result.aspect_ratio == "999:999"

    # Invalid image URL - treated as extra parameter
    result = parser.parse_dict({"text": "a photo", "image": "not_a_url"})
    assert len(result.image_prompts) == 0
    assert result.extra_params.get("image") == "not_a_url"


def test_empty_values():
    """Test handling of empty values."""
    parser = MidjourneyParser()

    # Empty text
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": ""})

    # Empty image list
    prompt = parser.parse_dict({"text": "a photo", "image_prompts": []})
    assert prompt.text == "a photo"
    assert not prompt.image_prompts

    # None values
    prompt = parser.parse_dict({"text": "a photo", "stylize": None})
    assert prompt.text == "a photo"
    assert prompt.stylize == DEFAULT_STYLIZE  # Default value


def test_version_parameter():
    """Test parsing of version parameter."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "version": "6",
        }
    )

    assert prompt.text == "a photo"
    assert prompt.version == "v6"


def test_multiple_permutations():
    """Test handling of multiple permutations."""
    parser = MidjourneyParser()

    # Test with parameter permutations
    input_dicts = [
        {"text": "smooth edges", "stylize": "75"},
        {"text": "smooth edges", "stylize": "300"},
        {"text": "smooth edges", "stylize": "75", "personalization": True},
        {"text": "smooth edges", "stylize": "300", "personalization": True},
    ]

    results = [parser.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {(r.text.strip(), r.stylize, r.personalization) for r in results}

    expected = {
        ("smooth edges", 75.0, False),
        ("smooth edges", 300.0, False),
        ("smooth edges", 75.0, True),
        ("smooth edges", 300.0, True),
    }

    assert result_tuples == expected

    # Test with flag permutations
    input_dicts = [
        {"text": "photo"},
        {"text": "photo", "tile": True},
        {"text": "photo", "turbo": True},
        {"text": "photo", "tile": True, "turbo": True},
    ]

    results = [parser.parse_dict(d) for d in input_dicts]
    assert len(results) == 4

    # Verify each permutation is handled correctly
    result_tuples = {(r.text.strip(), r.tile, r.turbo) for r in results}

    expected = {
        ("photo", False, False),
        ("photo", True, False),
        ("photo", False, True),
        ("photo", True, True),
    }

    assert result_tuples == expected


def test_personalization_parameter():
    """Test parsing of personalization parameter."""
    parser = MidjourneyParser()

    # Test flag with True value
    prompt = parser.parse_dict({"text": "a photo", "personalization": True})
    assert prompt.personalization is True

    # Test flag with False value
    prompt = parser.parse_dict({"text": "a photo", "personalization": False})
    assert prompt.personalization is False


def test_edge_cases():
    """Test handling of edge cases in Midjourney parser."""
    parser = MidjourneyParser()

    # Test empty prompt
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": ""})

    # Test prompt with only spaces
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": "   "})

    # Test prompt with special characters
    prompt = parser.parse_dict({"text": "a photo with special characters !@#$%^&*()"})
    assert prompt.text == "a photo with special characters !@#$%^&*()"

    # Test prompt with long text
    long_text = "a" * 1000
    prompt = parser.parse_dict({"text": long_text})
    assert prompt.text == long_text

    # Test prompt with mixed types in extra parameters
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "extra1": "123",
            "extra2": "45.67",
            "extra3": "true",
            "extra4": None,
            "extra5": "item1",
        }
    )
    assert prompt.extra_params["extra1"] == "123"
    assert prompt.extra_params["extra2"] == "45.67"
    assert prompt.extra_params["extra3"] == "true"
    assert prompt.extra_params["extra4"] is None
    assert prompt.extra_params["extra5"] == "item1"
