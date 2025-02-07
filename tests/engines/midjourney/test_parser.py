"""Tests for Midjourney parser."""

import pytest

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
    assert prompt.stylize == STYLIZE_VALUE
    assert prompt.seed == SEED_VALUE
    assert prompt.chaos == CHAOS_VALUE


def test_style_parameters():
    """Test parsing of style parameters."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict({"text": "a photo", "style": "raw", "v": VERSION_NUMBER})

    assert prompt.text == "a photo"
    assert prompt.style == "raw"
    assert prompt.version == f"v{VERSION_NUMBER}"


def test_aspect_ratio():
    """Test parsing of aspect ratio."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict({"text": "a photo", "aspect": "16:9"})

    assert prompt.text == "a photo"
    assert prompt.aspect_width == 16
    assert prompt.aspect_height == 9


def test_image_prompts():
    """Test parsing of image prompts."""
    parser = MidjourneyParser()
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = parser.parse_dict({"text": "a fusion", "images": urls})

    assert prompt.text == "a fusion"
    assert len(prompt.image_prompts) == 2
    assert [p.url for p in prompt.image_prompts] == urls


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
            "iw": str(IMAGE_WEIGHT_VALUE),
        }
    )

    assert prompt.text == "a photo"
    assert prompt.stylize == STYLIZE_VALUE
    assert prompt.seed == SEED_VALUE
    assert prompt.image_weight == IMAGE_WEIGHT_VALUE


def test_invalid_values():
    """Test handling of invalid parameter values."""
    parser = MidjourneyParser()

    # Invalid aspect ratio - now accepts any value
    result = parser.parse_dict({"text": "a photo", "aspect": "999:999"})
    assert result.aspect_width == 999
    assert result.aspect_height == 999

    # Invalid numeric value - raises ValueError
    with pytest.raises(ValueError, match=r"Invalid numeric value for stylize: 1001"):
        parser.parse_dict({"text": "a photo", "stylize": "1001"})

    # Invalid image URL - treated as extra parameter
    result = parser.parse_dict({"text": "a photo", "image": "not_a_url"})
    assert len(result.image_prompts) == 0
    assert result.extra_params.get("image") == "not_a_url"


def test_parameter_ranges():
    """Test parameter value range validation."""
    parser = MidjourneyParser()

    # Test maximum values
    with pytest.raises(ValueError, match=r"Invalid numeric value for stylize: 2000"):
        parser.parse_dict({"text": "a photo", "stylize": "2000"})

    # Test minimum values
    with pytest.raises(ValueError, match=r"Invalid numeric value for chaos: -1"):
        parser.parse_dict({"text": "a photo", "chaos": "-1"})


def test_empty_values():
    """Test handling of empty values."""
    parser = MidjourneyParser()

    # Empty text
    with pytest.raises(ValueError, match="Empty prompt"):
        parser.parse_dict({"text": ""})

    # Empty image list
    prompt = parser.parse_dict({"text": "a photo", "images": []})
    assert prompt.text == "a photo"
    assert not prompt.image_prompts

    # None values
    prompt = parser.parse_dict({"text": "a photo", "stylize": None})
    assert prompt.text == "a photo"
    assert prompt.stylize is None


def test_niji_parameter():
    """Test parsing of niji parameter."""
    parser = MidjourneyParser()
    prompt = parser.parse_dict(
        {
            "text": "a photo",
            "niji": "6",
        }
    )

    assert prompt.text == "a photo"
    assert prompt.version == "niji 6"
