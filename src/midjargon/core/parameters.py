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
    Validate a parameter value.

    Args:
        name: Parameter name.
        value: Parameter value to validate.

    Raises:
        ValueError: If value is invalid for the parameter type.
    """
    if value is None:
        return

    # Handle list values for reference parameters
    if isinstance(value, list):
        if name not in {"character_reference", "style_reference"}:
            msg = f"List values only allowed for reference parameters, got: {name}"
            raise ValueError(msg)
        for item in value:
            if not any(
                item.lower().endswith(ext) for ext in {".jpg", ".jpeg", ".png", ".gif"}
            ):
                msg = f"Invalid reference file extension for {name}: {item}"
                raise ValueError(msg)
        return

    # Validate numeric parameters
    if name in {
        "stylize",
        "chaos",
        "weird",
        "image_weight",
        "quality",
        "character_weight",
        "style_weight",
        "repeat",
    }:
        try:
            num = float(value)
            if num < 0:
                msg = f"Parameter {name} cannot be negative: {value}"
                raise ValueError(msg)
        except ValueError as e:
            msg = f"Invalid numeric value for {name}: {value}"
            raise ValueError(msg) from e

    # Validate version parameter
    if name == "version":
        if not value.replace(".", "").isdigit() and not value.startswith("niji"):
            msg = f"Invalid version value: {value}"
            raise ValueError(msg)

    # Validate reference parameters
    if name in {"character_reference", "style_reference"}:
        if not any(
            value.lower().endswith(ext) for ext in {".jpg", ".jpeg", ".png", ".gif"}
        ):
            msg = f"Invalid reference file extension for {name}: {value}"
            raise ValueError(msg)


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
        ext in value.lower() for ext in {".jpg", ".jpeg", ".png", ".gif"}
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
    current_param = ""
    current_values = []

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

        # Process value
        if is_flag:
            if value is None:
                params[expanded_name] = None
            else:
                params[expanded_name] = value
        else:
            if value is not None:
                processed_value = process_param_value([value])
                validate_param_value(expanded_name, processed_value)

                # Handle reference parameters specially
                if (
                    expanded_name in {"character_reference", "style_reference"}
                    and processed_value
                ):
                    # Convert comma-separated list to actual list
                    params[expanded_name] = [
                        f.strip() for f in processed_value.split(",")
                    ]
                else:
                    params[expanded_name] = processed_value
            else:
                msg = f"Missing value for parameter: {name}"
                raise ValueError(msg)

    return params
