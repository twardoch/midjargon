#!/usr/bin/env python3
# this_file: tests/integration/test_workflow.py

"""Integration tests for the complete workflow."""

from __future__ import annotations

import sys
from io import StringIO

import pytest

from midjargon.cli.main import MidjargonCLI
from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt_to_dict


def process_prompt(prompt: str) -> list[dict]:
    """Process a prompt through the complete workflow.

    Args:
        prompt: The prompt to process.

    Returns:
        List of dictionaries representing the processed prompts.
    """
    variants = expand_midjargon_input(prompt)
    results = []
    for variant in variants:
        results.append(parse_midjargon_prompt_to_dict(variant.prompt.to_string()))
    return results


def test_basic_workflow():
    """Test basic prompt processing workflow."""
    prompt = "a portrait --ar 16:9 --stylize 200"
    results = process_prompt(prompt)

    assert len(results) == 1
    assert results[0]["text"] == "a portrait"
    assert results[0]["aspect_ratio"] == "16:9"
    assert results[0]["stylize"] == 200


def test_permutation_workflow():
    """Test workflow with permutations."""
    prompt = "a {red, blue} bird"
    results = process_prompt(prompt)

    assert len(results) == 2
    assert any("red" in r["text"] for r in results)
    assert any("blue" in r["text"] for r in results)


def test_image_workflow():
    """Test workflow with image URLs."""
    prompt = "https://example.com/image.jpg a portrait"
    results = process_prompt(prompt)

    assert len(results) == 1
    assert len(results[0]["image_prompts"]) == 1
    assert str(results[0]["image_prompts"][0]) == "https://example.com/image.jpg"


def test_parameter_workflow():
    """Test workflow with various parameters."""
    prompt = "portrait --ar 16:9 --stylize 200 --chaos 50 --v 6"
    results = process_prompt(prompt)

    assert len(results) == 1
    assert results[0]["text"] == "portrait"
    assert results[0]["aspect_ratio"] == "16:9"
    assert results[0]["stylize"] == 200
    assert results[0]["chaos"] == 50
    assert results[0]["version"] == "v6"


def test_new_parameters_workflow():
    """Test workflow with newer parameters."""
    prompt = "portrait --cref https://example.com/char.jpg --cw 50"
    results = process_prompt(prompt)

    assert len(results) == 1
    assert len(results[0]["character_reference"]) == 1
    assert results[0]["character_weight"] == 50


def test_weighted_prompts_workflow():
    """Test workflow with weighted prompts."""
    prompt = "first prompt::0.7 second prompt::0.3"
    results = process_prompt(prompt)

    assert len(results) == 2
    weights = [r.get("weight", 1.0) for r in results]
    assert 0.7 in weights
    assert 0.3 in weights


def test_error_workflow():
    """Test workflow error handling."""
    with pytest.raises(ValueError):
        process_prompt("portrait --ar invalid")


def test_complex_workflow():
    """Test workflow with complex combinations."""
    prompt = "a {red, blue} bird::0.6 a {green, yellow} tree::0.4"
    results = process_prompt(prompt)

    assert len(results) == 4
    colors = set()
    for r in results:
        text = r["text"].lower()
        if "red" in text:
            colors.add("red")
        if "blue" in text:
            colors.add("blue")
        if "green" in text:
            colors.add("green")
        if "yellow" in text:
            colors.add("yellow")
    assert colors == {"red", "blue", "green", "yellow"}


def test_permutations_with_parameters():
    """Test permutations with parameters."""
    prompt = "photo {modern, vintage} --ar {1:1, 16:9} --s 100"
    results = process_prompt(prompt)

    # Convert results to set of tuples for easier comparison
    result_tuples = {
        (r["text"].strip(), r["aspect_ratio"], r["stylize"]) for r in results
    }

    expected = {
        ("photo modern", "1:1", 100),
        ("photo modern", "16:9", 100),
        ("photo vintage", "1:1", 100),
        ("photo vintage", "16:9", 100),
    }
    assert result_tuples == expected


def test_permutations_with_flag_parameters():
    """Test permutations with flag parameters (no value) are handled correctly."""
    prompt = "photo {, --tile} {, --turbo}"
    results = process_prompt(prompt)

    # Convert results to set of tuples for easier comparison
    result_tuples = {
        (r["text"].strip(), r.get("tile", False), r.get("turbo", False))
        for r in results
    }

    expected = {
        ("photo", False, False),
        ("photo", False, True),
        ("photo", True, False),
        ("photo", True, True),
    }
    assert result_tuples == expected


def test_permutations_with_complex_parameters():
    """Test permutations with complex parameter combinations."""
    prompt = "portrait {modern, vintage} {, --p custom} --ar {1:1, 16:9} --s 100"
    results = process_prompt(prompt)

    # Convert results to set of tuples for easier comparison
    result_tuples = {
        (
            r["text"].strip(),
            (
                r["personalization"][0]
                if isinstance(r.get("personalization", []), list)
                else r.get("personalization")
            ),
            f"{r['aspect_width']}:{r['aspect_height']}",
            r["stylize"],
        )
        for r in results
    }

    expected = {
        ("portrait modern", None, "1:1", 100),
        ("portrait modern", "custom", "1:1", 100),
        ("portrait modern", None, "16:9", 100),
        ("portrait modern", "custom", "16:9", 100),
        ("portrait vintage", None, "1:1", 100),
        ("portrait vintage", "custom", "1:1", 100),
        ("portrait vintage", None, "16:9", 100),
        ("portrait vintage", "custom", "16:9", 100),
    }
    assert result_tuples == expected


def test_cli_mj_command():
    """Test Midjourney prompt conversion using CLI."""
    cli = MidjargonCLI()
    prompt = "a serene landscape --ar 16:9 --stylize 100"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.mj(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        output = capture_stdout.getvalue()
    assert "serene landscape" in output
    assert "16:9" in output
    assert "100" in output


def test_cli_fal_command():
    """Test Fal.ai prompt conversion using CLI."""
    cli = MidjargonCLI()
    prompt = "a serene landscape --ar 16:9 --stylize 100"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.fal(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        output = capture_stdout.getvalue()
    assert "serene landscape" in output
    assert "16:9" in output
    assert "100" in output


def test_cli_perm_command():
    """Test permutation expansion using CLI."""
    cli = MidjargonCLI()
    prompt = "a {red, blue} bird on a {branch, rock}"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        cli.perm(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        output = capture_stdout.getvalue()
    assert "red" in output
    assert "blue" in output
    assert "branch" in output
    assert "rock" in output
