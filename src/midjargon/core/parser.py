"""
parser.py

Provides a simple, permissive parser that converts an expanded prompt (a MidjargonPrompt string)
into a flat dictionary (MidjargonDict) with the following keys:
  - "images": list of image URLs (extracted from the beginning of the prompt)
  - "text": the main text of the prompt
  - Additional keys for any parameters found (keys without the '--' prefix)

This parser does not perform strict validation; it only tokenizes and groups values.
"""

import re
from typing import cast

from .parameters import parse_parameters
from .type_defs import MidjargonDict, MidjargonPrompt


def _split_text_and_params(text: str) -> tuple[str, str]:
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
            return text[:i].strip(), text[i:]
        i += 1
    return text.strip(), ""


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


def parse_midjargon_prompt_to_dict(expanded_prompt: MidjargonPrompt) -> MidjargonDict:
    """
    Parses an expanded prompt string (with no permutation syntax) into a dictionary.

    The resulting dictionary will contain:
    - 'images': List of image URLs found at the start of the prompt
    - 'text': The main text content of the prompt
    - Additional keys for any parameters found (without the '--' prefix)

    Args:
        expanded_prompt: A prompt string that has been expanded (i.e., no outstanding permutations).

    Returns:
        MidjargonDict: Dict with keys 'images', 'text', and additional parameter keys.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not expanded_prompt.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    # Split into tokens
    tokens = expanded_prompt.split()

    # Extract image URLs
    urls, remaining = parse_image_urls(tokens)

    # Split remaining text into main text and parameters
    main_text = " ".join(remaining)
    text_part, param_part = _split_text_and_params(main_text)

    # Validate that there is actual text content
    if not text_part and not urls:
        msg = "Prompt must contain text or image URLs"
        raise ValueError(msg)

    # Parse parameters using the consolidated parameter parsing logic
    params = parse_parameters(param_part) if param_part.startswith("--") else {}

    # Build the dictionary according to the specification
    result = {
        "images": urls,
        "text": text_part,
        **params,  # Merge additional parameters directly into the dict
    }

    return cast(MidjargonDict, result)
