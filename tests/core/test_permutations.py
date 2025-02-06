#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest"]
# ///

"""Tests for permutation handling functionality."""

from midjargon.core.permutations import expand_permutations, split_options


def test_simple_permutation():
    """Test basic permutation expansion."""
    text = "a {red, blue} bird"
    results = expand_permutations(text)
    assert set(results) == {"a red bird", "a blue bird"}


def test_multiple_permutations():
    """Test handling of multiple permutation groups."""
    text = "a {red, blue} bird on a {flower, leaf}"
    results = expand_permutations(text)
    expected = {
        "a red bird on a flower",
        "a red bird on a leaf",
        "a blue bird on a flower",
        "a blue bird on a leaf",
    }
    assert set(results) == expected


def test_nested_permutations():
    """Test handling of nested permutation groups."""
    text = "a {big {red, blue}, small green} bird"
    results = expand_permutations(text)
    expected = {"a big red bird", "a big blue bird", "a small green bird"}
    assert set(results) == expected


def test_escaped_characters():
    """Test handling of escaped characters in permutations."""
    text = "a {red\\, blue, green} bird"
    results = expand_permutations(text)
    assert set(results) == {"a red, blue bird", "a green bird"}


def test_empty_options():
    """Test handling of empty options in permutations."""
    text = "a {, red, } bird"
    results = expand_permutations(text)
    assert set(results) == {"a bird", "a red bird"}


def test_single_option():
    """Test handling of single option in permutations."""
    text = "a {red} bird"
    results = expand_permutations(text)
    assert set(results) == {"a red bird"}


def test_split_permutation_options():
    """Test splitting of permutation options."""
    text = "red, blue, green"
    options = split_options(text)
    assert options == ["red", "blue", "green"]

    # Test with escaped comma
    text = "red\\, blue, green"
    options = split_options(text)
    assert options == ["red, blue", "green"]


def test_invalid_permutations():
    """Test handling of invalid permutation syntax."""
    # Unclosed brace - should be treated as literal
    result = expand_permutations("a {red, blue bird")
    assert result == ["a {red, blue bird"]

    # Unopened brace - should be treated as literal
    result = expand_permutations("a red} bird")
    assert result == ["a red} bird"]

    # Double nested group - should be expanded normally
    result = expand_permutations("a {{red}} bird")
    assert result == ["a red bird"]


def test_permutations_with_parameters():
    """Test permutations with parameters are preserved."""
    text = "a {red, blue} bird --ar 16:9"
    results = expand_permutations(text)
    assert all("--ar 16:9" in result for result in results)


def test_complex_nested_permutations():
    """Test complex nested permutation scenarios."""
    text = "a {big {red, blue} {cat, dog}, small {green, yellow} bird}"
    results = expand_permutations(text)
    expected = {
        "a big red cat",
        "a big red dog",
        "a big blue cat",
        "a big blue dog",
        "a small green bird",
        "a small yellow bird",
    }
    assert set(results) == expected
