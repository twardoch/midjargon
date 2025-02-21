#!/usr/bin/env python3
# this_file: tests/test_core.py

import pytest

from midjargon import expand_midjargon_input
from midjargon.core.models import (
    MidjourneyParameters,
    MidjourneyPrompt,
)
from midjargon.core.parser import parse_midjargon_prompt
from midjargon.core.permutations import expand_permutations


def test_basic_prompt_parsing():
    """Test basic prompt parsing without parameters."""
    prompt = "a beautiful landscape"
    result = parse_midjargon_prompt(prompt)
    assert isinstance(result, MidjourneyPrompt)
    assert result.text == "a beautiful landscape"
    assert not result.image_prompts
    assert result.parameters == MidjourneyParameters()


def test_prompt_with_parameters():
    """Test prompt parsing with various parameters."""
    prompt = "a portrait --ar 16:9 --stylize 200 --chaos 50 --v 6"
    result = parse_midjargon_prompt(prompt)

    assert result.text == "a portrait"
    assert result.parameters.aspect == "16:9"
    assert result.parameters.stylize == 200
    assert result.parameters.chaos == 50
    assert result.parameters.version == "v6"


def test_prompt_with_image():
    """Test prompt parsing with image URLs."""
    prompt = "https://example.com/image.jpg a photo in this style"
    result = parse_midjargon_prompt(prompt)

    assert result.text == "a photo in this style"
    assert len(result.image_prompts) == 1
    assert str(result.image_prompts[0]) == "https://example.com/image.jpg"


def test_invalid_parameters():
    """Test handling of invalid parameters."""
    with pytest.raises(ValueError):
        parse_midjargon_prompt("test --invalid value")


def test_permutation_expansion():
    """Test permutation expansion."""
    prompt = "a {red, blue} bird on a {green, yellow} tree"
    results = expand_permutations(prompt)

    assert len(results) == 4
    assert "a red bird on a green tree" in results
    assert "a red bird on a yellow tree" in results
    assert "a blue bird on a green tree" in results
    assert "a blue bird on a yellow tree" in results


def test_escaped_permutations():
    """Test handling of escaped characters in permutations."""
    prompt = r"a {red\, orange, blue} bird"
    results = expand_permutations(prompt)

    assert len(results) == 2
    assert "a red, orange bird" in results
    assert "a blue bird" in results


def test_weighted_prompts():
    """Test handling of weighted prompts."""
    prompt = "first prompt::0.7 second prompt::0.3"
    results = expand_midjargon_input(prompt)

    assert len(results) == 2
    assert results[0].weight == 0.7
    assert results[1].weight == 0.3


def test_combined_features():
    """Test combination of multiple features."""
    prompt = "a {red, blue} bird::0.6 a {green, yellow} tree::0.4"
    results = expand_midjargon_input(prompt)

    assert len(results) == 4
    # Check first group
    red_blue = [r for r in results if "bird" in r.prompt.text]
    assert len(red_blue) == 2
    assert all("bird" in r.prompt.text for r in red_blue)
    assert all(r.weight == 0.6 for r in red_blue)

    # Check second group
    green_yellow = [r for r in results if "tree" in r.prompt.text]
    assert len(green_yellow) == 2
    assert all("tree" in r.prompt.text for r in green_yellow)
    assert all(r.weight == 0.4 for r in green_yellow)


def test_style_reference():
    """Test handling of style references."""
    # Test with code
    prompt = "test --sref p123456"
    result = parse_midjargon_prompt(prompt)
    assert result.style_reference
    assert result.style_reference[0].code == "p123456"

    # Test with URL
    prompt = "test --sref https://example.com/style.jpg"
    result = parse_midjargon_prompt(prompt)
    assert result.style_reference
    assert str(result.style_reference[0].url) == "https://example.com/style.jpg"


def test_character_reference():
    """Test handling of character references."""
    prompt = "test --cref https://example.com/char.jpg --cw 50"
    result = parse_midjargon_prompt(prompt)

    assert result.character_reference
    assert str(result.character_reference[0].url) == "https://example.com/char.jpg"
    assert result.character_weight == 50


def test_prompt_to_string():
    """Test conversion of prompt back to string format."""
    original = "a portrait --ar 16:9 --stylize 200"
    result = parse_midjargon_prompt(original)

    # Convert back to string
    output = result.to_string()

    # Parse again to verify equivalence
    reparsed = parse_midjargon_prompt(output)
    assert reparsed.text == result.text
    assert reparsed.parameters.model_dump() == result.parameters.model_dump()
