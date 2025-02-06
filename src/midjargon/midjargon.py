#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic"]
# ///

"""
midjargon.py

Core module for parsing Midjourney-style prompts.
Coordinates between permutations, parameters, and prompt structure.
"""

import re
from dataclasses import dataclass

from .parameters import parse_parameters
from .permutations import expand_text


@dataclass
class MidjargonPrompt:
    """Represents a parsed Midjourney-style prompt before parameter validation."""

    text: str  # The main text portion
    parameters: dict[str, str | None]  # Raw parameters and their values
    image_urls: list[str]  # List of image URLs at the start of prompt


def _split_text_and_params(text: str) -> tuple[str, str]:
    """Split text into main text and parameters at first non-nested --."""
    i = 0
    depth = 0
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        elif (
            text[i : i + 2] == "--" and depth == 0 and (i == 0 or text[i - 1].isspace())
        ):
            return text[:i].strip(), text[i:]
        i += 1
    return text.strip(), ""


def _combine_text_and_params(
    text_expanded: list[str], param_expanded: list[str]
) -> list[str]:
    """Combine expanded text and parameter permutations."""
    result = []
    for t in text_expanded:
        for p in param_expanded:
            result.append(f"{t} {p}".strip())
    return result


def expand_permutations(text: str) -> list[str]:
    """
    Expands all permutations in curly braces into separate complete prompts.
    Handles nested permutations and parameters.

    Args:
        text: The prompt text potentially containing {} permutations.

    Returns:
        List of expanded prompts with all permutations resolved.
    """
    # Split into text and parameters
    main_text, params = _split_text_and_params(text)

    # Expand text permutations
    text_expanded = expand_text(main_text)

    # If no parameters, return expanded text
    if not params:
        return text_expanded

    # Expand parameter permutations
    param_expanded = expand_text(params)

    # Combine text and parameter permutations
    return _combine_text_and_params(text_expanded, param_expanded)


def _find_parameter_split(text: str) -> int:
    """Find index where parameters start."""
    i = 0
    depth = 0
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        elif (
            text[i : i + 2] == "--" and depth == 0 and (i == 0 or text[i - 1].isspace())
        ):
            return i
        i += 1
    return len(text)


def _validate_parts(parts: list[str]) -> None:
    """Validate parts of a prompt."""
    if not parts:
        msg = "Empty prompt"
        raise ValueError(msg)

    # Check for unmatched braces
    total_open = sum(1 for part in parts for char in part if char == "{")
    total_close = sum(1 for part in parts for char in part if char == "}")
    if total_open != total_close:
        msg = "Unmatched braces in prompt"
        raise ValueError(msg)

    # Check for invalid parameter format
    for part in parts:
        if part.startswith("--") and len(part) == 2:
            msg = "Invalid parameter format: empty parameter name"
            raise ValueError(msg)
        if part.startswith("--") and not part[2:].replace("-", "").isalnum():
            msg = f"Invalid parameter format: {part}"
            raise ValueError(msg)


def split_text_and_parameters(text: str) -> tuple[str, str]:
    """
    Split prompt text into main text and parameter portions.

    Args:
        text: Raw prompt text.

    Returns:
        Tuple of (main_text, parameter_text).
    """
    # Split at first non-nested parameter marker
    split_idx = _find_parameter_split(text)
    main_text = text[:split_idx].strip()
    param_text = text[split_idx:].strip()

    return main_text, param_text


def parse_image_urls(tokens: list[str]) -> tuple[list[str], list[str]]:
    """
    Extract image URLs from the start of tokens.

    Args:
        tokens: List of tokens from prompt text.

    Returns:
        Tuple of (image_urls, remaining_tokens).
    """
    urls = []
    i = 0

    url_pattern = re.compile(
        r"^https?://[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif|webp)$", re.IGNORECASE
    )

    # Extract URLs from start of tokens
    while i < len(tokens):
        token = tokens[i]
        if url_pattern.match(token):
            urls.append(token)
            i += 1
        else:
            break

    return urls, tokens[i:]


def parse_prompt(prompt: str) -> list[MidjargonPrompt]:
    """
    Parse a prompt string into structured components.
    Handles permutations by returning multiple prompts if needed.

    Args:
        prompt: Raw prompt string.

    Returns:
        List of parsed MidjargonPrompt objects.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not prompt.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    results = []

    # First expand any permutations
    expanded = expand_permutations(prompt)

    for exp_prompt in expanded:
        # Split into tokens
        tokens = exp_prompt.split()
        _validate_parts(tokens)

        # Extract image URLs
        urls, remaining = parse_image_urls(tokens)

        # Split remaining text into main text and parameters
        main_text = " ".join(remaining)
        text_part, param_part = split_text_and_parameters(main_text)

        # Validate that there is actual text content
        if not text_part and not urls:
            msg = "Prompt must contain text or image URLs"
            raise ValueError(msg)

        # Parse parameters
        params = parse_parameters(param_part)

        # Create prompt object
        prompt_obj = MidjargonPrompt(
            text=text_part,
            parameters=params,
            image_urls=urls,
        )

        results.append(prompt_obj)

    return results
