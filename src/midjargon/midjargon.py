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


def expand_permutations(text: str) -> list[str]:
    """
    Expands all permutations in curly braces into separate complete prompts.
    Handles nested permutations and parameters.

    Args:
        text: The prompt text potentially containing {} permutations.

    Returns:
        List of expanded prompts with all permutations resolved.
    """

    def find_matching_brace(s: str, start: int) -> int:
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

    def expand_single_permutation(text: str) -> list[str]:
        """Expands a single level of permutation."""
        results = []
        i = 0

        while i < len(text):
            if text[i] == "{":
                end = find_matching_brace(text, i)
                if end == -1:
                    # Unmatched brace - treat as literal
                    results = [text]
                    break

                before = text[:i].rstrip()  # Remove trailing spaces
                options = split_permutation_options(text[i + 1 : end])
                after = text[end + 1 :].lstrip()  # Remove leading spaces

                # Add space after 'before' if it ends with a word character and isn't empty
                if before and before[-1].isalnum():
                    before = before + " "
                # Add space before 'after' if it starts with a word character and isn't empty
                if after and after[0].isalnum():
                    after = " " + after

                # Recursively expand any nested permutations in each option
                expanded_options = []
                for opt in options:
                    if "{" in opt:
                        expanded = expand_single_permutation(opt)
                        expanded_options.extend(expanded)
                    else:
                        expanded_options.append(opt)

                # Combine with before/after text
                results = []
                for opt in expanded_options:
                    # Handle parameters in permutations
                    if opt.startswith("--"):
                        # Parameter permutation - keep the space before
                        results.append(f"{before}{opt}{after}")
                    # Regular permutation
                    elif not opt:
                        # For empty option, just combine before and after
                        results.append(f"{before}{after}".strip())
                    else:
                        # For non-empty option, add the option
                        results.append(f"{before}{opt}{after}".strip())
                break
            i += 1

        # No permutations found
        if not results:
            results = [text]

        return [
            r.strip() for r in results
        ]  # Strip any extra whitespace from final results

    # First split into text and parameters at the first non-nested --
    text_parts = []
    param_parts = []

    i = 0
    depth = 0
    text_start = 0
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        elif (
            text[i : i + 2] == "--" and depth == 0 and (i == 0 or text[i - 1].isspace())
        ):
            if i > text_start:
                text_parts.append(text[text_start:i].strip())
            param_parts.append(text[i:])
            break
        i += 1
    else:
        if text_start < len(text):
            text_parts.append(text[text_start:].strip())

    # Expand text permutations
    text_expanded = []
    if text_parts:
        current = [text_parts[0]]
        while any("{" in t for t in current):
            next_level = []
            for t in current:
                next_level.extend(expand_single_permutation(t))
            current = next_level
        text_expanded = current
    else:
        text_expanded = [""]

    # Expand parameter permutations
    param_expanded = []
    if param_parts:
        param_text = param_parts[0]

        # Split into individual parameter groups
        param_groups = []
        i = 0
        depth = 0
        param_start = 0

        while i < len(param_text):
            if param_text[i] == "{":
                depth += 1
            elif param_text[i] == "}":
                depth -= 1
            elif (
                param_text[i : i + 2] == "--"
                and depth == 0
                and (i == 0 or param_text[i - 1].isspace())
            ):
                if i > param_start:
                    param_groups.append(param_text[param_start:i].strip())
                param_start = i
            i += 1

        if param_start < len(param_text):
            param_groups.append(param_text[param_start:].strip())

        # Expand each parameter group
        expanded_groups = []
        for group in param_groups:
            current = [group]
            while any("{" in p for p in current):
                next_level = []
                for p in current:
                    expanded = expand_single_permutation(p)
                    next_level.extend(expanded)
                current = next_level
            expanded_groups.append(current)

        # Generate all combinations of parameter groups
        from itertools import product

        if expanded_groups:
            combinations = list(product(*expanded_groups))
            param_expanded = [" ".join(p for p in combo if p) for combo in combinations]
        else:
            param_expanded = [""]

    else:
        param_expanded = [""]

    # Combine all text and parameter combinations
    results = []
    for text_part in text_expanded:
        for param_part in param_expanded:
            if param_part:
                results.append(f"{text_part} {param_part}")
            else:
                results.append(text_part)

    return results


def parse_parameters(param_str: str) -> dict[str, str | None]:
    """
    Parses parameter strings into a dictionary.

    Args:
        param_str: String containing parameters (each beginning with '--').
        A parameter followed immediately by another parameter has no value (boolean flag).
        A parameter followed by non-parameter tokens uses those tokens as its value.

    Returns:
        Dictionary mapping parameter names to their values (or None if no value).

    Raises:
        ValueError: If the parameter string is invalid or malformed.
    """
    if not param_str:
        return {}

    # Check for invalid parameter format
    if param_str == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)

    params = {}
    tokens = param_str.split()
    i = 0
    current_param = None
    current_values = []

    while i < len(tokens):
        token = tokens[i]

        if token.startswith("--"):
            # Validate parameter name
            param_name = token[2:].lower()
            if not param_name:
                msg = "Empty parameter name"
                raise ValueError(msg)
            if not param_name.replace("-", "").isalnum():
                msg = f"Invalid parameter name: {param_name}"
                raise ValueError(msg)

            # Save previous parameter if any
            if current_param is not None:
                value = " ".join(current_values) if current_values else None
                if value and value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]  # Remove surrounding quotes
                params[current_param] = value

            # Start new parameter
            current_param = param_name
            current_values = []
            i += 1
        else:
            # Add value to current parameter
            if current_param is not None:
                current_values.append(token)
            else:
                msg = "Value without parameter"
                raise ValueError(msg)
            i += 1

    # Save last parameter
    if current_param is not None:
        value = " ".join(current_values) if current_values else None
        if value and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]  # Remove surrounding quotes
        # Check if the last parameter has a required value
        if not value and current_param not in [
            "tile",
            "raw",
        ]:  # Add known flag parameters here
            msg = f"Missing required value for parameter: {current_param}"
            raise ValueError(msg)
        params[current_param] = value

    return params


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

    # Pattern to split on first whitespace followed by '--'
    # that is not inside a permutation block
    parts = []
    current = []
    i = 0
    depth = 0  # Track brace depth

    while i < len(text):
        if text[i] == "{":
            depth += 1
            current.append(text[i])
        elif text[i] == "}":
            depth -= 1
            current.append(text[i])
        elif (
            text[i : i + 2] == "--" and depth == 0 and (i == 0 or text[i - 1].isspace())
        ):
            if current:
                parts.append("".join(current).strip())
                current = []
            current.append(text[i:])
            break
        else:
            current.append(text[i])
        i += 1

    if current:
        parts.append("".join(current).strip())

    if len(parts) == 1:
        # Check if the only part starts with '--'
        if parts[0].startswith("--"):
            msg = "Prompt contains only parameters"
            raise ValueError(msg)
        return parts[0], ""
    else:
        return parts[0], parts[1]


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
