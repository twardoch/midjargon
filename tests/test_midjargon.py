#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest"]
# ///

"""Tests for the midjargon module."""

import pytest

from midjargon import MidjargonPrompt, parse_prompt

# Constants for test assertions
PERMUTATION_COMBINATIONS = 4  # 2x2 combinations for red/blue x flower/leaf
ESCAPED_COMMA_OPTIONS = 2  # "red, blue" and "green"
NESTED_PERMUTATION_OPTIONS = 3  # "big red", "big blue", "small green"
MULTIPLE_IMAGE_URLS = 2  # Number of test image URLs


def test_basic_prompt():
    """Test parsing of a basic prompt without any special features."""
    prompt = "a serene landscape --ar 16:9 --stylize 100"
    result = parse_prompt(prompt)
    assert len(result) == 1
    parsed = result[0]
    assert isinstance(parsed, MidjargonPrompt)
    assert parsed.text == "a serene landscape"
    assert parsed.parameters["ar"] == "16:9"
    assert parsed.parameters["stylize"] == "100"
    assert not parsed.image_urls


def test_prompt_with_image_url():
    """Test parsing of a prompt with an image URL."""
    prompt = "https://example.com/image.jpg mystical forest --chaos 20"
    result = parse_prompt(prompt)
    assert len(result) == 1
    parsed = result[0]
    assert parsed.text == "mystical forest"
    assert parsed.parameters["chaos"] == "20"
    assert len(parsed.image_urls) == 1
    assert parsed.image_urls[0] == "https://example.com/image.jpg"


def test_permutation_prompt():
    """Test expansion of permutation prompts."""
    prompt = "a {red, blue} bird on a {flower, leaf} --ar 16:9"
    results = parse_prompt(prompt)
    assert len(results) == PERMUTATION_COMBINATIONS
    texts = {result.text for result in results}
    expected = {
        "a red bird on a flower",
        "a red bird on a leaf",
        "a blue bird on a flower",
        "a blue bird on a leaf",
    }
    assert texts == expected
    # All variations should have the same parameters
    for result in results:
        assert result.parameters["ar"] == "16:9"


def test_multi_prompt_with_weights():
    """Test parsing of multi-prompts with weights."""
    prompt = "mystical forest ::2 foggy mountains ::1 --chaos 20"
    result = parse_prompt(prompt)
    assert len(result) == 1
    parsed = result[0]
    assert "mystical forest ::2 foggy mountains ::1" in parsed.text
    assert parsed.parameters["chaos"] == "20"


def test_parameter_without_value():
    """Test parsing of parameters without values (flags)."""
    prompt = "landscape photo --tile --no blur,cars"
    result = parse_prompt(prompt)
    assert len(result) == 1
    parsed = result[0]
    assert parsed.text == "landscape photo"
    assert parsed.parameters["tile"] is None  # Flag parameter
    assert parsed.parameters["no"] == "blur,cars"


def test_escaped_commas_in_permutations():
    """Test handling of escaped commas in permutation options."""
    prompt = "a {red\\, blue, green} bird"
    result = parse_prompt(prompt)
    assert len(result) == ESCAPED_COMMA_OPTIONS
    texts = {r.text for r in result}
    assert texts == {"a red, blue bird", "a green bird"}


def test_nested_permutations():
    """Test handling of nested permutation groups."""
    prompt = "a {big {red, blue}, small green} bird"
    result = parse_prompt(prompt)
    assert len(result) == NESTED_PERMUTATION_OPTIONS
    texts = {r.text for r in result}
    assert texts == {"a big red bird", "a big blue bird", "a small green bird"}


def test_multiple_image_urls():
    """Test parsing of multiple image URLs."""
    prompt = "https://example.com/1.jpg https://example.com/2.jpg forest --iw 2"
    result = parse_prompt(prompt)
    assert len(result) == 1
    parsed = result[0]
    assert len(parsed.image_urls) == MULTIPLE_IMAGE_URLS
    assert parsed.parameters["iw"] == "2"


def test_invalid_prompt():
    """Test handling of invalid prompts."""
    with pytest.raises(ValueError):
        parse_prompt("")  # Empty prompt

    with pytest.raises(ValueError):
        parse_prompt("--ar 16:9")  # Only parameters, no text
