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


@pytest.fixture
def capture_stdout():
    """Capture stdout for testing."""
    stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout
    try:
        yield stdout
    finally:
        sys.stdout = old_stdout
        stdout.seek(0)  # Reset buffer position


@pytest.fixture
def capture_stderr():
    """Capture stderr for testing."""
    stderr = StringIO()
    old_stderr = sys.stderr
    sys.stderr = stderr
    yield stderr
    sys.stderr = old_stderr


def parse_json_output(output: str) -> Any:
    """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
    # Remove ANSI escape sequences
    output = ANSI_ESCAPE.sub("", output)
    output = output.strip()
    if not output:
        raise ValueError("No JSON found in output")
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        raise ValueError("No JSON found in output")


def test_basic_prompt(capture_stdout):
    """Test basic prompt processing."""
    main(f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT}", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a beautiful landscape"
    assert prompt["aspect_width"] == ASPECT_WIDTH
    assert prompt["aspect_height"] == ASPECT_HEIGHT


def test_permutations(capture_stdout):
    """Test permutation processing."""
    main("a {red, blue} bird", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 2
    texts = {p["text"] for p in data}
    assert texts == {"a red bird", "a blue bird"}


def test_raw_output(capture_stdout):
    """Test raw output mode."""
    main(f"a photo --stylize {STYLIZE_VALUE}", raw=True, json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a photo"
    assert prompt["stylize"] == str(STYLIZE_VALUE)


def test_json_output_formatting(capture_stdout):
    """Test JSON output formatting."""
    main("a photo", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 1


def test_invalid_input(capture_stdout):
    """Test handling of invalid input."""
    with pytest.raises(SystemExit):
        main("", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert "error" in data


def test_parameter_validation(capture_stdout):
    """Test parameter validation."""
    with pytest.raises(SystemExit):
        main(f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True)  # Over max
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert "error" in data


def test_image_url_handling(capture_stdout):
    """Test handling of image URLs."""
    url = "https://example.com/image.jpg"
    main(f"{url} a fusion", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 1
    prompt = data[0]
    assert prompt["text"] == "a fusion"
    assert len(prompt["image_prompts"]) == 1
    assert prompt["image_prompts"][0]["url"] == url


def test_no_color_output(capture_stdout):
    """Test no-color output mode."""
    Console(force_terminal=False)
    main("a photo", json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == 1


def test_complex_prompt(capture_stdout):
    """Test complex prompt with multiple features."""
    prompt = (
        "https://example.com/img1.jpg https://example.com/img2.jpg "
        "a {red, blue} bird on a {branch, rock} "
        f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} --chaos {CHAOS_VALUE}"
    )
    main(prompt, json_output=True)
    output = capture_stdout.getvalue()
    data = parse_json_output(output)
    assert isinstance(data, list)
    assert len(data) == PERMUTATION_COUNT_2X2
    for prompt in data:
        assert len(prompt["image_prompts"]) == IMAGE_PROMPTS_COUNT
        assert prompt["stylize"] == STYLIZE_VALUE
        assert prompt["chaos"] == CHAOS_VALUE
        assert prompt["aspect_width"] == ASPECT_WIDTH
        assert prompt["aspect_height"] == ASPECT_HEIGHT
