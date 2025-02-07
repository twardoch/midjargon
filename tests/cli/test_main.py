#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest", "rich"]
# ///

"""Tests for CLI functionality."""

import json
import re
import sys
from io import StringIO
from typing import Any

import pytest
from rich.console import Console

from midjargon.cli.main import main

# Test constants
ASPECT_WIDTH = 16
ASPECT_HEIGHT = 9
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
IMAGE_PROMPTS_COUNT = 2
PERMUTATION_COUNT_2X2 = 4  # 2 options x 2 options

ANSI_ESCAPE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")


def parse_json_output(output_stream: StringIO) -> Any:
    """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
    output_stream.seek(0)
    output = output_stream.getvalue()
    # Remove ANSI escape sequences
    output = ANSI_ESCAPE.sub("", output)
    output = output.strip()
    if not output:
        msg = "No JSON found in output"
        raise ValueError(msg)
    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        msg = "No JSON found in output"
        raise ValueError(msg) from e


def test_basic_prompt():
    """Test basic prompt processing."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main(
            f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT}",
            json_output=True,
        )
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a beautiful landscape"
    assert prompt["aspect_width"] == ASPECT_WIDTH
    assert prompt["aspect_height"] == ASPECT_HEIGHT


def test_permutations():
    """Test permutation processing."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main("a {red, blue} bird", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 2
    texts = {p["text"] for p in data}
    assert texts == {"a red bird", "a blue bird"}


def test_raw_output():
    """Test raw output mode."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main(f"a photo --stylize {STYLIZE_VALUE}", raw=True, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a photo"
    assert prompt["stylize"] == STYLIZE_VALUE


def test_json_output_formatting():
    """Test JSON output formatting."""
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main("a photo", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 1


def test_invalid_input():
    """Test handling of invalid input."""
    with StringIO() as capture_stdout:
        with pytest.raises(SystemExit):
            sys.stdout = capture_stdout
            main("", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
        assert "error" in data


def test_parameter_validation():
    """Test parameter validation."""
    with StringIO() as capture_stdout:
        with pytest.raises(SystemExit):
            sys.stdout = capture_stdout
            main(
                f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True
            )  # Over max
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
        assert "error" in data


def test_image_url_handling():
    """Test handling of image URLs."""
    url = "https://example.com/image.jpg"
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main(f"{url} a fusion", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a fusion"
    assert len(prompt["image_prompts"]) == 1
    assert prompt["image_prompts"][0]["url"] == url


def test_no_color_output():
    """Test no-color output mode."""
    Console(force_terminal=False)
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main("a photo", json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == 1


def test_complex_prompt():
    """Test complex prompt with multiple features."""
    prompt = (
        "https://example.com/img1.jpg https://example.com/img2.jpg "
        "a {red, blue} bird on a {branch, rock} "
        f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} --chaos {CHAOS_VALUE}"
    )
    with StringIO() as capture_stdout:
        sys.stdout = capture_stdout
        main(prompt, json_output=True)
        sys.stdout = sys.__stdout__
        data = parse_json_output(capture_stdout)
    assert isinstance(data, list)
    assert len(data) == PERMUTATION_COUNT_2X2
    for prompt in data:
        assert len(prompt["image_prompts"]) == IMAGE_PROMPTS_COUNT
        assert prompt["stylize"] == STYLIZE_VALUE
        assert prompt["chaos"] == CHAOS_VALUE
        assert prompt["aspect_width"] == ASPECT_WIDTH
        assert prompt["aspect_height"] == ASPECT_HEIGHT
