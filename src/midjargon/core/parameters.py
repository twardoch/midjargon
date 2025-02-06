#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic"]
# ///

"""
parameters.py

Handles parsing and validation of Midjourney prompt parameters.
This module provides a unified interface for parameter handling,
supporting both raw string parsing and structured parameter handling.
"""

from typing import TypeAlias

# Type aliases for clarity
ParamName: TypeAlias = str
ParamValue: TypeAlias = str | None
ParamDict: TypeAlias = dict[ParamName, ParamValue]

# Common parameter shortcuts
PARAM_SHORTCUTS = {
    # Basic parameters
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "ar": "ar",  # Keep ar as is to match test expectations
    "no": None,  # Flag parameter
    "tile": None,  # Flag parameter
    # Quality parameters
    "q": "quality",
    # Reference parameters
    "cref": "character_reference",
    "sref": "style_reference",
    "cw": "character_weight",
    "sw": "style_weight",
    "sv": "style_version",
    # Repeat parameter
    "r": "repeat",
    # Mode flags
    "turbo": None,  # Flag parameter
    "relax": None,  # Flag parameter
}

# Constants
NIJI_PREFIX_LENGTH = 4  # Length of "niji" in version string


def validate_param_name(name: str) -> None:
    """
    Basic validation of a parameter name.

    Args:
        name: Parameter name to validate.

    Raises:
        ValueError: If name is empty or contains invalid characters.
    """
    if not name:
        msg = "Empty parameter name"
        raise ValueError(msg)
    if not name.replace("-", "").replace("_", "").isalnum():
        msg = f"Invalid parameter name: {name}"
        raise ValueError(msg)


def process_param_value(values: list[str]) -> str | None:
    """
    Process parameter values into a single value.

    Args:
        values: List of parameter value parts.

    Returns:
        Processed parameter value or None.
    """
    if not values:
        return None
    value = " ".join(values)
    # Remove surrounding quotes if present
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  # Remove surrounding quotes
    elif value.startswith("'") and value.endswith("'"):
        value = value[1:-1]  # Remove surrounding quotes
    return value


def expand_shorthand_param(name: str) -> tuple[str, bool]:
    """
    Expand a shorthand parameter name to its full form.

    Args:
        name: Parameter name that might be in shorthand form.

    Returns:
        Tuple of (expanded_name, is_flag_param).
    """
    # Handle special case for niji versions
    if name.startswith("niji"):
        return "version", False

    # Handle special case for personalization
    if name == "p" or name.startswith("p "):
        return "personalization", False

    # Handle version shorthand
    if name == "v" or name.startswith("v "):
        return "version", False

    # Look up in shortcuts
    if name in PARAM_SHORTCUTS:
        expanded = PARAM_SHORTCUTS[name]
        return (name if expanded is None else expanded, expanded is None)

    return name, False


def _expand_param_name(name: str) -> str:
    """
    Expand parameter shorthand to full name.

    Args:
        name: Parameter shorthand or full name.

    Returns:
        Full parameter name.
    """
    shorthand_map = {
        "s": "stylize",
        "c": "chaos",
        "w": "weird",
        "iw": "image_weight",
        "q": "quality",
        "cw": "character_weight",
        "sw": "style_weight",
        "sv": "style_version",
        "p": "personalization",
        "v": "version",
        "ar": "ar",  # Keep ar as is
        "cref": "character_reference",
        "sref": "style_reference",
        "no": "no",  # Keep no as is
    }
    return shorthand_map.get(name, name)


def _process_param_chunk(
    chunk: str, params: dict[str, str | None]
) -> tuple[str, str | None]:
    """
    Process a parameter chunk into name and value.

    Args:
        chunk: Parameter chunk to process.
        params: Dictionary to store parameters in.

    Returns:
        Tuple of (parameter name, parameter value).

    Raises:
        ValueError: If chunk is invalid.
    """
    if not chunk:
        msg = "Empty parameter chunk"
        raise ValueError(msg)

    # Split on first space
    parts = chunk.split(maxsplit=1)
    name = parts[0].lstrip("-")

    # Handle flag parameters (no value)
    if len(parts) == 1:
        if name in {"tile", "turbo", "relax"}:
            return name, None
        if name == "niji":
            return "version", "niji"
        if name == "p":
            return "personalization", ""
        if name.startswith("no"):
            return "no", name[2:]  # Remove no prefix
        return name, None

    # Handle value parameters
    value = parts[1]
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  # Remove quotes

    # Handle special cases where parameters might be combined
    if "--" in value:
        # Split on -- and process each part
        value_parts = value.split("--")
        # Only take the first part as the value for this parameter
        value = value_parts[0].strip()
        # Process remaining parts as new parameters
        for part in value_parts[1:]:
            # Add the -- prefix back and process recursively
            name_part, value_part = _process_param_chunk(f"--{part.strip()}", params)
            if name_part:
                params[name_part] = value_part

    expanded_name = _expand_param_name(name)

    # Special handling for niji parameter
    if expanded_name == "niji" and value.isdigit():
        return "version", f"niji {value}"

    # Special handling for personalization parameter
    if expanded_name in ("personalization", "p"):
        # Remove any trailing parameters if present
        if "--" in value:
            value = value.split("--")[0].strip()
        return "personalization", value

    # Special handling for version parameter
    if expanded_name in ("version", "v"):
        if not value:
            return "version", None
        if value.startswith("niji"):
            return "version", value
        return "version", value if value.startswith("v") else f"v{value}"

    return expanded_name, value


def parse_parameters(param_str: str) -> dict[str, str | None]:
    """
    Parse parameter string into a dictionary.

    Args:
        param_str: Parameter string to parse.

    Returns:
        Dictionary of parameter names and values.

    Raises:
        ValueError: If parameters are invalid.
    """
    if not param_str:
        return {}

    # Split on spaces, preserving quoted strings
    chunks = []
    current_chunk = []
    in_quotes = False
    quote_char = None

    for char in param_str:
        if char in {'"', "'"}:
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            current_chunk.append(char)
        elif char.isspace() and not in_quotes:
            if current_chunk:
                chunks.append("".join(current_chunk))
                current_chunk = []
        else:
            current_chunk.append(char)

    if current_chunk:
        chunks.append("".join(current_chunk))

    # Process each parameter chunk
    params = {}
    current_chunk = []

    for chunk in chunks:
        if chunk.startswith("--"):
            if current_chunk:
                name, value = _process_param_chunk(" ".join(current_chunk), params)
                if name:  # Only add if name is not empty
                    params[name] = value
                current_chunk = []
            current_chunk.append(chunk)
        else:
            current_chunk.append(chunk)

    if current_chunk:
        name, value = _process_param_chunk(" ".join(current_chunk), params)
        if name:  # Only add if name is not empty
            params[name] = value

    return params
