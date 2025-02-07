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
ParamValue: TypeAlias = str | list[str] | None
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
    if name.startswith("-"):
        msg = f"Parameter name cannot start with dash: {name}"
        raise ValueError(msg)


def validate_param_value(name: str, value: ParamValue) -> None:
    """
    Basic syntactic validation of a parameter value.
    Semantic validation is handled by the engine layer.

    Args:
        name: Parameter name.
        value: Parameter value to validate.

    Raises:
        ValueError: If value has invalid syntax.
    """
    if value is None:
        return

    # Handle list values
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, str):
                msg = f"List values must be strings, got: {type(item)}"
                raise ValueError(msg)
        return

    # Validate numeric parameters can be converted to float
    if name in {
        "stylize",
        "chaos",
        "weird",
        "image_weight",
        "quality",
        "character_weight",
        "style_weight",
        "style_version",
        "repeat",
        "seed",
        "stop",
    }:
        try:
            float(value)
        except ValueError as e:
            msg = f"Invalid numeric value for {name}: {value}"
            raise ValueError(msg) from e


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
        return "version", True

    # Handle special case for version parameter
    if name == "v":
        return "version", False

    # Handle special case for personalization
    if name == "p":
        return "personalization", True

    # Check for shorthand in mapping
    if name in PARAM_SHORTCUTS:
        expanded = PARAM_SHORTCUTS[name]
        return (expanded if expanded else name, expanded is None)

    return name, False


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

    # Handle version parameter specially
    if value.startswith("v") and value[1:].replace(".", "").isdigit():
        return value[1:]  # Strip 'v' prefix for version numbers
    elif value.startswith("niji"):
        return value  # Keep niji version as is

    # Handle reference files
    if "," in value and any(
        ext in value.lower() for ext in (".jpg", ".jpeg", ".png", ".gif")
    ):
        # Split on commas and clean up each file path
        files = [f.strip() for f in value.split(",")]
        return ",".join(files)

    return value


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
    Basic syntactic processing only - semantic validation is handled by the engine layer.

    Args:
        chunk: Parameter chunk to process.
        params: Dictionary to store parameters in.

    Returns:
        Tuple of (parameter name, parameter value).

    Raises:
        ValueError: If chunk has invalid syntax.
    """
    if not chunk:
        msg = "Empty parameter chunk"
        raise ValueError(msg)

    # Split on first space
    parts = chunk.split(maxsplit=1)
    name = parts[0].lstrip("-")

    # Handle flag parameters (no value)
    if len(parts) == 1:
        # Basic parameter name expansion, no semantic validation
        if name == "niji":
            return "version", "niji"
        if name == "p":
            return "personalization", ""
        if name.startswith("no"):
            return "no", name[2:]
        return name, None

    # Handle value parameters
    value = parts[1]
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  # Remove quotes

    # Handle special cases where parameters might be combined
    if "--" in value:
        value_parts = value.split("--")
        value = value_parts[0].strip()
        for part in value_parts[1:]:
            name_part, value_part = _process_param_chunk(f"--{part.strip()}", params)
            if name_part:
                params[name_part] = value_part

    expanded_name = _expand_param_name(name)

    # Basic parameter name expansion, no semantic validation
    if expanded_name == "niji" and value.isdigit():
        return "version", f"niji {value}"

    if expanded_name in ("personalization", "p"):
        if "--" in value:
            value = value.split("--")[0].strip()
        return "personalization", value

    return expanded_name, value


def parse_parameters(param_str: str) -> ParamDict:
    """
    Parse parameter string into a dictionary.

    Args:
        param_str: String containing parameters (e.g., "--ar 16:9 --stylize 100").

    Returns:
        Dictionary mapping parameter names to values.

    Raises:
        ValueError: If parameter format is invalid.
    """
    params: ParamDict = {}

    # Split into chunks and process each
    chunks = param_str.split("--")
    for chunk in chunks[1:]:  # Skip first empty chunk
        if not chunk.strip():
            msg = "Empty parameter"
            raise ValueError(msg)

        # Split at first space to separate name and value
        parts = chunk.strip().split(maxsplit=1)
        name = parts[0]
        value = parts[1] if len(parts) > 1 else None

        # Validate and expand parameter name
        validate_param_name(name)
        expanded_name, is_flag = expand_shorthand_param(name)

        # If the parameter requires a value (not a flag) but none was provided, raise an error
        if not is_flag and value is None:
            raise ValueError(f"Missing required value for parameter: {name}")

        # Process value
        if is_flag:
            if value is None:
                if expanded_name == "version":
                    params[expanded_name] = "niji"  # Default for --niji
                elif expanded_name == "personalization":
                    params[expanded_name] = ""  # Default for --p
                else:
                    params[expanded_name] = None
            else:
                params[expanded_name] = value
        elif value is not None:
            processed_value = process_param_value([value])
            validate_param_value(expanded_name, processed_value)

            # Handle reference parameters specially
            if (
                expanded_name in {"character_reference", "style_reference"}
                and processed_value
            ):
                # Convert comma-separated list to actual list
                params[expanded_name] = processed_value
            else:
                params[expanded_name] = processed_value
        else:
            msg = f"Missing value for parameter: {name}"
            raise ValueError(msg)

    return params
