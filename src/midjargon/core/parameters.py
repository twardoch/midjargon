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
    "ar": "aspect",  # Keep ar as is to match test expectations
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
    if name == "niji":
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
        "ar": "aspect",  # Keep ar as is
        "cref": "character_reference",
        "sref": "style_reference",
        "no": "no",  # Keep no as is
    }
    return shorthand_map.get(name, name)


def _process_flag_param(name: str) -> tuple[str, str | None]:
    """Process a flag parameter (no value)."""
    if name == "niji":
        return "version", "niji"
    if name == "p":
        return "personalization", ""
    if name.startswith("no"):
        return "no", name[2:]
    return name, None


def _process_value_with_dashes(value: str, params: dict[str, str | None]) -> str:
    """Process a value that contains double dashes."""
    value_parts = value.split("--")
    result_value = value_parts[0].strip()
    for part in value_parts[1:]:
        name_part, value_part = _process_param_chunk(f"--{part.strip()}", params)
        if name_part:
            params[name_part] = value_part
    return result_value


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
    if not chunk or chunk == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)

    # Split on first space
    parts = chunk.split(maxsplit=1)
    name = parts[0].lstrip("-")

    # Validate parameter name
    validate_param_name(name)

    # Handle flag parameters (no value)
    if len(parts) == 1:
        # Special case for version and personalization which require values
        if name in ["v", "version"]:
            msg = "Missing required value for version parameter"
            raise ValueError(msg)
        return _process_flag_param(name)

    # Handle value parameters
    value = parts[1]
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]  # Remove quotes

    # Handle special cases where parameters might be combined
    if "--" in value:
        value = _process_value_with_dashes(value, params)

    expanded_name = _expand_param_name(name)

    # Basic parameter name expansion, no semantic validation
    if expanded_name == "niji" and value.isdigit():
        return "version", f"niji {value}"

    if expanded_name in ("personalization", "p"):
        if "--" in value:
            value = value.split("--")[0].strip()
        return "personalization", value

    return expanded_name, value


def _split_into_chunks(param_str: str) -> list[str]:
    """Split parameter string into chunks, handling quoted values."""
    chunks = []
    current_chunk = []
    in_quotes = False
    quote_char = None

    for char in param_str:
        if char in ('"', "'"):
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

    if in_quotes:
        msg = "Unclosed quotes in parameters"
        raise ValueError(msg)

    return chunks


def _process_current_param(
    current_param: str | None,
    current_values: list[str],
    params: ParamDict,
) -> None:
    """Process and store the current parameter."""
    if current_param is None:
        return

    # Validate that required parameters have values
    expanded_name, is_flag = expand_shorthand_param(current_param)
    if not is_flag and not current_values:
        msg = f"Missing value for parameter: {current_param}"
        raise ValueError(msg)

    # Process and store the parameter
    value = process_param_value(current_values)
    validate_param_value(expanded_name, value)
    if expanded_name == "version" and current_param == "niji":
        params[expanded_name] = "niji" if value is None else f"niji {value}"
    else:
        params[expanded_name] = value


def parse_parameters(param_str: str) -> ParamDict:
    """
    Parse a parameter string into a dictionary.

    Args:
        param_str: String containing parameters (e.g., "--ar 16:9 --stylize 100").

    Returns:
        Dictionary mapping parameter names to values.

    Raises:
        ValueError: If parameter format is invalid.
    """
    if not param_str:
        return {}

    # Initialize parameters dictionary
    params: ParamDict = {}

    # Split into chunks (handling quoted values)
    chunks = _split_into_chunks(param_str)

    # Process chunks
    current_param = None
    current_values = []

    for chunk in chunks:
        # Validate that parameters start with --
        if not current_param and not chunk.startswith("--"):
            msg = "Parameter must start with -- prefix"
            raise ValueError(msg)

        if chunk.startswith("--"):
            # Process previous parameter if exists
            _process_current_param(current_param, current_values, params)
            current_param = chunk[2:]  # Remove leading --
            current_values = []
        else:
            current_values.append(chunk)

    # Process the last parameter
    _process_current_param(current_param, current_values, params)

    return params
