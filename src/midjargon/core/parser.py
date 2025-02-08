"""
parser.py

Provides a simple, permissive parser that converts an expanded prompt (a MidjargonPrompt string)
into a flat dictionary (MidjargonDict) with the following keys:
  - "images": list of image URLs (extracted from the beginning of the prompt)
  - "text": the main text of the prompt
  - Additional keys for any parameters found (keys without the '--' prefix)

This parser does not perform strict validation; it only tokenizes and groups values.
"""

import contextlib
import re
from dataclasses import dataclass
from typing import cast

from midjargon.core.parameters import parse_parameters
from midjargon.core.type_defs import MidjargonDict, MidjargonPrompt


@dataclass
class TextPart:
    """Represents a part of text with its whitespace."""

    text: str
    leading_space: str = ""
    trailing_space: str = ""


def unescape_text(text: str) -> str:
    """Remove escape characters while preserving intended characters."""
    # Replace escaped braces and commas with temporary markers
    text = text.replace(r"\{", "\x00").replace(r"\}", "\x01").replace(r"\,", "\x02")

    # Remove other escape characters
    text = re.sub(r"\\(.)", r"\1", text)

    # Restore escaped characters
    text = text.replace("\x00", "{").replace("\x01", "}").replace("\x02", ",")

    return text


def split_text_and_parameters(text: str) -> tuple[str, str]:
    """
    Split text into main text and parameters at first non-nested --.

    Args:
        text: The text to split.

    Returns:
        Tuple of (main_text, parameter_text).
        If no parameters are found, parameter_text will be empty.
    """
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
            return text[:i].rstrip(), text[i:]
        i += 1
    return text.rstrip(), ""


def parse_image_urls(tokens: list[str]) -> tuple[list[str], list[str]]:
    """
    Extract image URLs from the start of tokens.

    Args:
        tokens: List of tokens from prompt text.

    Returns:
        Tuple of (image_urls, remaining_tokens).
        Image URLs are extracted from the start of tokens until a non-URL token is found.
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


def parse_text_parts(text: str) -> list[TextPart]:
    """Parse text into parts while preserving whitespace."""
    parts = []
    current = ""
    leading_space = ""
    i = 0

    while i < len(text):
        # Handle whitespace
        if text[i].isspace():
            if not current:
                leading_space += text[i]
            else:
                current += text[i]
            i += 1
            continue

        # Handle regular characters
        if text[i] not in "{}":
            current += text[i]
            i += 1
            continue

        # Handle braces
        if text[i] == "{":
            # Add current part if any
            if current:
                trailing_space = ""
                while current and current[-1].isspace():
                    trailing_space = current[-1] + trailing_space
                    current = current[:-1]
                if current:
                    parts.append(TextPart(current, leading_space, trailing_space))
                leading_space = trailing_space
                current = ""

            # Find matching closing brace
            depth = 1
            j = i + 1
            while j < len(text) and depth > 0:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                j += 1

            if depth == 0:  # Found matching brace
                brace_content = text[i:j]
                if brace_content == "{}":  # Empty permutation
                    i = j
                    continue
                current = brace_content
                i = j
            else:  # No matching brace
                current += text[i]
                i += 1
        else:  # Closing brace without matching open
            current += text[i]
            i += 1

    # Add final part
    if current:
        trailing_space = ""
        while current and current[-1].isspace():
            trailing_space = current[-1] + trailing_space
            current = current[:-1]
        if current:
            parts.append(TextPart(current, leading_space, trailing_space))

    return parts


def parse_midjargon_prompt_to_dict(expanded_prompt: MidjargonPrompt) -> MidjargonDict:
    """
    Parse an expanded prompt into a dictionary format.
    Handles URL extraction and parameter parsing.

    Args:
        expanded_prompt: Expanded prompt string.

    Returns:
        Dictionary containing parsed prompt components.
    """
    # Extract URLs and text
    urls = []
    text_parts = []

    # First pass: extract URLs
    parts = expanded_prompt.split()
    url_pattern = re.compile(
        r"^https?://[^\s/$.?#].[^\s]*\.(jpg|jpeg|png|gif|webp)$", re.IGNORECASE
    )

    for part in parts:
        if url_pattern.match(part):
            urls.append(part)
        else:
            text_parts.append(part)

    # Rejoin text parts and split into text and parameters
    text_part = " ".join(text_parts)
    main_text, param_part = split_text_and_parameters(text_part)

    # Handle escaped characters and empty permutations
    main_text = unescape_text(main_text)
    main_text = re.sub(r"\{\s*\}", "", main_text)  # Remove empty permutations
    main_text = re.sub(r"\s+", " ", main_text).strip()  # Normalize whitespace

    # Parse parameters using the consolidated parameter parsing logic
    params = parse_parameters(param_part) if param_part.startswith("--") else {}

    # Convert numeric values
    numeric_params = {
        "stylize": int,
        "chaos": int,
        "weird": int,
        "image_weight": float,
        "seed": int,
        "stop": int,
        "quality": float,
        "repeat": int,
        "character_weight": int,
        "style_weight": int,
        "style_version": int,
    }

    for param, converter in numeric_params.items():
        if param in params and params[param] is not None:
            with contextlib.suppress(ValueError, TypeError):
                params[param] = converter(params[param])

    # Build the dictionary according to the specification
    result = {
        "images": urls,
        "text": main_text,
        **params,  # Merge additional parameters directly into the dict
    }

    return cast(MidjargonDict, result)
