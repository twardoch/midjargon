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
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "ar": "aspect",
    "no": None,  # Flag parameter
    "tile": None,  # Flag parameter
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
    if not name.replace("-", "").isalnum():
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


def _validate_param_string(param_str: str) -> None:
    """Validate the parameter string format."""
    if not param_str:
        return

    if not param_str.startswith("--"):
        msg = "Parameters must start with --"
        raise ValueError(msg)

    if param_str == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)


def _handle_special_params(
    name: str, raw_value: str | None, expanded_name: str
) -> tuple[str, str | None]:
    """Handle special parameter cases."""
    # Handle special case for niji version
    if name.startswith("niji"):
        value = (
            name[NIJI_PREFIX_LENGTH:].strip() if len(name) > NIJI_PREFIX_LENGTH else ""
        )
        return expanded_name, f"niji{value}"

    # Handle special case for personalization
    if name == "p":
        return expanded_name, raw_value or ""

    # Handle version parameter
    if name == "v":
        return expanded_name, raw_value

    return expanded_name, raw_value


def _process_param_chunk(chunk: str) -> tuple[str, str | None]:
    """Process a single parameter chunk."""
    parts = chunk.split(None, 1)
    if not parts:
        msg = "Empty parameter name"
        raise ValueError(msg)

    name = parts[0]
    raw_value = parts[1] if len(parts) > 1 else None

    # Expand shorthand and handle flag parameters
    expanded_name, is_flag = expand_shorthand_param(name)
    validate_param_name(expanded_name)

    # Handle flag parameters (--no, --tile)
    if is_flag:
        return expanded_name, None

    # Handle special cases
    expanded_name, value = _handle_special_params(name, raw_value, expanded_name)

    # Handle quotes if present
    if value and value.startswith(('"', "'")) and value.endswith(value[0]):
        value = value[1:-1]

    return expanded_name, value


def parse_parameters(param_str: str) -> ParamDict:
    """
    Parse parameter string into a dictionary of parameter names and values.
    Handles both full and shorthand parameter names.

    Args:
        param_str: String containing parameters (starting with --).

    Returns:
        Dictionary mapping parameter names to their raw values.

    Raises:
        ValueError: If parameter string is malformed.
    """
    params: ParamDict = {}
    if not param_str:
        return params

    _validate_param_string(param_str)

    # Split into chunks and process each one
    chunks = [c.strip() for c in param_str.split("--") if c.strip()]
    for chunk in chunks:
        name, value = _process_param_chunk(chunk)
        params[name] = value

    return params
