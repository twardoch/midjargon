#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pytest", "pydantic"]
# ///

"""Integration tests for complete midjargon workflow."""


import pytest

from midjargon import expand_midjargon_input, parse_midjargon_prompt_to_dict
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict

# Test constants
ASPECT_WIDTH = 16
ASPECT_HEIGHT = 9
STYLIZE_VALUE = 100
CHAOS_VALUE = 50
WEIRD_VALUE = 1000
SEED_VALUE = 12345
STOP_VALUE = 80
IMAGE_WEIGHT_VALUE = 2.0
PERMUTATION_COUNT_2X2 = 4  # 2 options x 2 options
PERMUTATION_COUNT_2X2X2 = 8  # 2 options x 2 options x 2 options


def process_prompt(prompt: str) -> list[MidjourneyPrompt]:
    """Process a prompt through the complete workflow."""
    # Step 1: Expand permutations
    expanded = expand_midjargon_input(prompt)

    # Step 2: Parse each expanded prompt to a dictionary
    midjargon_dicts = [parse_midjargon_prompt_to_dict(p) for p in expanded]

    # Step 3: Convert each dictionary to a MidjourneyPrompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]


def test_basic_workflow():
    """Test basic prompt workflow without permutations."""
    prompt = f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "a beautiful landscape"
    assert result.aspect_width == ASPECT_WIDTH
    assert result.aspect_height == ASPECT_HEIGHT
    assert result.stylize == STYLIZE_VALUE


def test_permutation_workflow():
    """Test workflow with permutations."""
    prompt = f"a {{red, blue}} bird on a {{branch, rock}} --stylize {STYLIZE_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == PERMUTATION_COUNT_2X2  # 2x2 permutations
    texts = {r.text for r in results}
    expected = {
        "a red bird on a branch",
        "a red bird on a rock",
        "a blue bird on a branch",
        "a blue bird on a rock",
    }
    assert texts == expected
    assert all(r.stylize == STYLIZE_VALUE for r in results)


def test_image_workflow():
    """Test workflow with image URLs."""
    urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]
    prompt = f"{' '.join(urls)} abstract fusion --iw {IMAGE_WEIGHT_VALUE}"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "abstract fusion"
    assert len(result.image_prompts) == 2
    assert [p.url for p in result.image_prompts] == urls
    assert result.image_weight == IMAGE_WEIGHT_VALUE


def test_parameter_workflow():
    """Test workflow with various parameter types."""
    prompt = (
        "cyberpunk city --v 5.2 --style raw --niji 6 "
        f"--chaos {CHAOS_VALUE} --weird {WEIRD_VALUE} "
        f"--seed {SEED_VALUE} --stop {STOP_VALUE} --no --tile"
    )
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]

    assert result.text == "cyberpunk city"
    assert result.version == "v5.2"
    assert result.style == "raw"
    assert result.chaos == CHAOS_VALUE
    assert result.weird == WEIRD_VALUE
    assert result.seed == SEED_VALUE
    assert result.stop == STOP_VALUE
    assert result.extra_params == {"no": None, "tile": None}


def test_weighted_prompts_workflow():
    """Test workflow with weighted prompts."""
    prompt = "cyberpunk city::2 neon lights::1"
    results = process_prompt(prompt)

    assert len(results) == 1
    result = results[0]
    assert result.text == "cyberpunk city::2 neon lights::1"


def test_error_workflow():
    """Test error handling in workflow."""
    # Test empty prompt
    with pytest.raises(ValueError, match="Empty prompt"):
        process_prompt("")

    # Test invalid parameter value
    with pytest.raises(ValueError):
        process_prompt(f"photo --stylize {STYLIZE_VALUE * 20}")  # Over max

    # Test invalid image URL
    with pytest.raises(ValueError):
        process_prompt("http://example.com/image.txt photo")  # Wrong extension

    # Test malformed parameters
    with pytest.raises(ValueError):
        process_prompt("photo --ar")  # Missing value

    # Test unmatched braces
    with pytest.raises(ValueError):
        process_prompt("a {red, blue bird")


def test_complex_workflow():
    """Test workflow with multiple features combined."""
    prompt = (
        "https://example.com/img1.jpg https://example.com/img2.jpg "
        "a {vintage, modern} {portrait, landscape} "
        "with {warm, cool} tones "
        f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} "
        f"--chaos {CHAOS_VALUE} --v 5.2 --style raw"
    )
    results = process_prompt(prompt)

    # 2x2x2 = 8 permutations
    assert len(results) == PERMUTATION_COUNT_2X2X2

    # Check common attributes
    for result in results:
        assert len(result.image_prompts) == 2
        assert result.aspect_width == ASPECT_WIDTH
        assert result.aspect_height == ASPECT_HEIGHT
        assert result.stylize == STYLIZE_VALUE
        assert result.chaos == CHAOS_VALUE
        assert result.version == "v5.2"
        assert result.style == "raw"

    # Check text variations
    texts = {r.text for r in results}
    assert len(texts) == PERMUTATION_COUNT_2X2X2  # All combinations are unique
