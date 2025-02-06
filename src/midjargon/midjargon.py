#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic"]
# ///

"""
prompt_midjargon.py

Parses Midjourney-style prompts into their component parts, handling permutations.
This module focuses on syntax parsing without Midjourney-specific validation.
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class MidjargonPrompt:
    """Represents a parsed Midjourney-style prompt before parameter validation."""

    text: str  # The main text portion
    parameters: dict[str, str | None]  # Raw parameters and their values
    image_urls: list[str]  # List of image URLs at the start of prompt


def split_permutation_options(text: str) -> list[str]:
    """
    Splits permutation options handling escaped commas.

    Args:
        text: The text inside {} brackets containing comma-separated options.

    Returns:
        List of individual options with escaped commas unescaped.
    """
    options = []
    current = []
    i = 0
    depth = 0  # Track nested braces

    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            if text[i + 1] in (",", "{", "}"):
                current.append(text[i + 1])
                i += 2
            else:
                current.append(text[i])
                i += 1
        elif text[i] == "{":
            depth += 1
            current.append(text[i])
            i += 1
        elif text[i] == "}":
            depth -= 1
            current.append(text[i])
            i += 1
        elif text[i] == "," and depth == 0:
            # Add current option (empty or not) after stripping whitespace
            opt = "".join(current).strip()
            options.append(opt)
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1

    # Add the last option after stripping whitespace
    if current or not options:
        opt = "".join(current).strip()
        options.append(opt)

    return options


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


def _format_permutation_part(before: str, opt: str, after: str) -> str:
    if opt.startswith("--"):
        # For parameter permutations, preserve exact spacing
        return f"{before}{opt}{after}".strip()
    # Combine before, opt, and after and collapse multiple spaces
    return " ".join((before + opt + after).split())


def _add_word_spacing(before: str, after: str) -> tuple[str, str]:
    """Add spacing between words if needed."""
    if before and before[-1].isalnum():
        before = before + " "
    if after and after[0].isalnum():
        after = " " + after
    return before, after


def _expand_text_permutations(text: str) -> list[str]:
    """Expand permutations in the text part."""
    text_expanded = [text] if text else [""]
    while any("{" in t for t in text_expanded):
        next_level = []
        for t in text_expanded:
            next_level.extend(_expand_single_permutation(t))
        text_expanded = next_level
    return text_expanded


def _find_matching_brace(s: str, start: int) -> int:
    """Find the matching closing brace for an opening brace at start."""
    count = 1
    i = start + 1
    while i < len(s):
        if s[i] == "{":
            count += 1
        elif s[i] == "}":
            count -= 1
            if count == 0:
                return i
        i += 1
    return -1


def _expand_nested_options(options: list[str]) -> list[str]:
    """Recursively expand any nested permutations in options."""
    expanded_options = []
    for opt in options:
        if "{" in opt:
            expanded_options.extend(_expand_single_permutation(opt))
        else:
            expanded_options.append(opt)
    return expanded_options


def _expand_single_permutation(text: str) -> list[str]:
    """Expands a single level of permutation."""
    results = []
    i = 0

    while i < len(text):
        if text[i] == "{":
            end = _find_matching_brace(text, i)
            if end == -1:
                return [text]  # Unmatched brace - treat as literal

            before = text[:i].rstrip()
            options = split_permutation_options(text[i + 1 : end])
            after = text[end + 1 :].lstrip()

            before, after = _add_word_spacing(before, after)

            # Recursively expand any nested permutations in each option
            expanded_options = _expand_nested_options(options)

            # Combine with before/after text
            results = [
                _format_permutation_part(before, opt, after) for opt in expanded_options
            ]
            break
        i += 1

    # No permutations found
    if not results:
        results = [text]

    return [r.strip() for r in results]


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
    text_expanded = _expand_text_permutations(main_text)

    # If no parameters, return expanded text
    if not params:
        return text_expanded

    # Expand parameter permutations
    param_expanded = _expand_single_permutation(params)

    # Combine text and parameter permutations
    return _combine_text_and_params(text_expanded, param_expanded)


def _validate_param_name(param_name: str) -> None:
    """Validate a parameter name."""
    if not param_name:
        msg = "Empty parameter name"
        raise ValueError(msg)
    if not param_name.replace("-", "").isalnum():
        msg = f"Invalid parameter name: {param_name}"
        raise ValueError(msg)


def _process_param_value(values: list[str]) -> str | None:
    """Process parameter values into a single value."""
    if not values:
        return None
    value = " ".join(values)
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  # Remove surrounding quotes
    return value


def _validate_param_value(param: str, value: str | None) -> None:
    """Validate that a parameter has a value if required."""
    flag_params = {"tile", "raw"}  # Known flag parameters that don't require values
    if not value and param not in flag_params:
        msg = f"Missing required value for parameter: {param}"
        raise ValueError(msg)


def parse_parameters(param_str: str) -> dict[str, str | None]:
    """
    Parse parameter string into a dictionary of parameter names and values.
    Handles quoted values and flag parameters.

    Args:
        param_str: String containing parameters (--param value --flag).

    Returns:
        Dictionary of parameter names to values.

    Raises:
        ValueError: If parameter syntax is invalid.
    """
    tokens = param_str.split()
    params: dict[str, str | None] = {}

    i = 0
    current_param = None
    current_values = []

    while i < len(tokens):
        token = tokens[i]

        if token.startswith("--"):
            # Save previous parameter if any
            if current_param is not None:
                value = _process_param_value(current_values)
                _validate_param_value(current_param, value)
                params[current_param] = value

            # Start new parameter
            param_name = token[2:].lower()
            _validate_param_name(param_name)
            current_param = param_name
            current_values = []
        # Add value to current parameter
        elif current_param is not None:
            current_values.append(token)
        else:
            msg = "Value without parameter"
            raise ValueError(msg)
        i += 1

    # Save last parameter
    if current_param is not None:
        value = _process_param_value(current_values)
        _validate_param_value(current_param, value)
        params[current_param] = value

    return params


def _handle_numeric_param(name: str, value: str | None) -> tuple[str, Any]:
    """Handle numeric parameter conversion."""
    # Define parameter mappings with their default values and conversion functions
    param_map = {
        ("stylize", "s"): ("stylize", lambda v: int(v) if v else 100),
        ("chaos", "c"): ("chaos", lambda v: int(v) if v else 0),
        ("weird",): ("weird", lambda v: int(v) if v else 0),
        ("iw",): ("image_weight", lambda v: float(v) if v else 1.0),
        ("seed",): ("seed", lambda v: int(v) if v else None),
        ("stop",): ("stop", lambda v: int(v) if v else 100),
    }

    # Find matching parameter and convert value
    for aliases, (param_name, converter) in param_map.items():
        if name in aliases:
            return param_name, converter(value)

    return "", None


def _handle_style_param(name: str, value: str | None) -> tuple[str, str | None]:
    """Handle style parameter conversion."""
    if name == "style":
        return "style", value
    elif name == "v":
        return "version", f"v{value}"
    elif name == "niji":
        return "version", f"niji {value}" if value else "niji"
    return "", None


def _find_parameter_split(text: str) -> int:
    """Find the index where parameters start (first non-nested --)."""
    depth = 0  # Track brace depth
    i = 0
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
    return -1


def _validate_parts(parts: list[str]) -> None:
    """Validate the split parts of the prompt."""
    if not parts:
        msg = "Empty prompt"
        raise ValueError(msg)
    if len(parts) == 1 and parts[0].startswith("--"):
        msg = "Prompt contains only parameters"
        raise ValueError(msg)


def split_text_and_parameters(text: str) -> tuple[str, str]:
    """
    Splits remaining prompt text into the text description and parameters part.

    Args:
        text: The prompt string (after image URLs removed).

    Returns:
        Tuple of (text_description, parameters_string).

    Raises:
        ValueError: If the prompt is empty or contains only parameters.
    """
    if not text.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    # Find where parameters start
    split_index = _find_parameter_split(text)

    # Split text into parts
    if split_index == -1:
        parts = [text.strip()]
    else:
        parts = [text[:split_index].strip(), text[split_index:].strip()]

    # Validate parts
    _validate_parts(parts)

    # Return appropriate parts
    return (parts[0], parts[1]) if len(parts) > 1 else (parts[0], "")


def parse_image_urls(tokens: list[str]) -> tuple[list[str], list[str]]:
    """
    Extracts image URL tokens from the beginning of the token list.

    Args:
        tokens: List of tokens split by whitespace.

    Returns:
        Tuple containing:
            - List of image URLs parsed from the tokens
            - The remaining tokens after the image URLs
    """
    image_pattern = re.compile(
        r"^(https?://\S+\.(?:png|jpg|jpeg|gif|webp))$", re.IGNORECASE
    )

    images = []
    remaining = tokens.copy()

    while remaining:
        if image_pattern.match(remaining[0]):
            images.append(remaining.pop(0))
        else:
            break

    return images, remaining


def parse_prompt(prompt: str) -> list[MidjargonPrompt]:
    """
    Parses a Midjourney-style prompt into its component parts.
    Handles permutations by returning multiple prompts if needed.

    Args:
        prompt: The raw prompt string.

    Returns:
        List of MidjargonPrompt objects representing all permutations.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    # Check for empty prompt
    if not prompt or not prompt.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    # Remove any command prefix
    pattern = re.compile(r"^/imagine\s+prompt:\s*", re.IGNORECASE)
    cleaned_prompt = pattern.sub("", prompt.strip())

    # Check if prompt is still empty after cleaning
    if not cleaned_prompt:
        msg = "Empty prompt"
        raise ValueError(msg)

    # Split into tokens
    tokens = cleaned_prompt.split()

    # Extract image URLs from the beginning
    image_urls, remaining_tokens = parse_image_urls(tokens)

    # Check if we have any content after image URLs
    if not remaining_tokens:
        msg = "Prompt contains only image URLs"
        raise ValueError(msg)

    # Reconstruct remaining text
    remaining_text = " ".join(remaining_tokens)

    # Check if the remaining text is only parameters
    if remaining_text.lstrip().startswith("--"):
        msg = "Prompt contains only parameters"
        raise ValueError(msg)

    # First expand any permutations
    expanded_texts = expand_permutations(remaining_text)

    # Process each expanded text
    results = []
    for text in expanded_texts:
        text_part, param_part = split_text_and_parameters(text)
        params = parse_parameters(param_part)
        results.append(
            MidjargonPrompt(text=text_part, parameters=params, image_urls=image_urls)
        )

    return results
