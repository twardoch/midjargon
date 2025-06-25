#!/usr/bin/env python3
# this_file: src/midjargon/core/parameters.py
from __future__ import annotations

Handles parsing and validation of Midjourney prompt parameters.
This module provides a unified interface for parameter handling,
supporting both raw string parsing and structured parameter handling.
"""

from midjargon.core.models import (CharacterReference, MidjourneyVersion,
                                   StyleMode, StyleReference)
from pydantic import HttpUrl

# Parameter aliases mapping
ALIASES = {
    # Version aliases
    "v": "version",
    "ver": "version",
    "niji": "version",
    # Style aliases
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    # Seed aliases
    "sameseed": "seed",
    # Aspect ratio aliases
    "ar": "aspect_ratio",
    # Character reference aliases
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
    "video": None,  # Flag parameter
    "remix": None,  # Flag parameter
}

# Constants
NIJI_PREFIX_LENGTH = 4  # Length of "niji" in version string
SPECIAL_SEED_VALUES = {"random"}  # Special values for seed parameter

# Update the parameter aliases
PARAMETER_ALIASES = {
    "s": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "ar": "aspect",
    "p": "personalization",
    "v": "version",
    "q": "quality",
    "cw": "character_weight",
    "sw": "style_weight",
    "sv": "style_version",
    "r": "repeat",
    "cref": "character_reference",
    "sref": "style_reference",
}


# Parameters that should remain as strings
STRING_PARAMS = {"aspect_ratio", "negative_prompt"}

# Parameters that should be integers
INT_PARAMS = {"style_version", "repeat"}

# Special seed values
SPECIAL_SEED_VALUES = {"random", "none"}

    Raises:
        ValueError: If name is empty or contains invalid characters.
    """
    if not name:
        msg = "Empty parameter name"
        raise ValueError(msg)
    if not isinstance(name, str):
        msg = f"Parameter name must be a string, got: {type(name)}"
        raise TypeError(msg)
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

def convert_parameter_value(param: str, value: str | None) -> Any:
    """Convert a parameter value to the appropriate type."""
    # Handle flag parameters
    if param in FLAG_PARAMS:
        if value is None:
            return True
        val_lower = value.lower()
        if val_lower in {"true", "1", "yes", "on"}:
            return True
        if val_lower in {"false", "0", "no", "off"}:
            return False
        return bool(value)

    Raises:
        ValueError: If value has invalid syntax.
    """
    if value is None:
        return

    # Handle string parameters
    if param in STRING_PARAMS:
        return str(value)

    # Handle version parameter
    if param == "version":
        if value.lower() == "niji":
            return "niji"
        try:
            return MidjourneyVersion(value)
        except ValueError:
            msg = f"Invalid version value: {value}"
            raise ValueError(msg)

    # Handle seed parameter
    if param == "seed":
        if value.lower() in SPECIAL_SEED_VALUES:
            return value.lower()
        try:
            return int(value)
        except ValueError:
            msg = f"Invalid seed value: {value}"
            raise ValueError(msg)

    # Handle integer parameters
    if param in INT_PARAMS:
        try:
            return int(value)
        except ValueError:
            msg = f"Invalid integer value for {param}: {value}"
            raise ValueError(msg)

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

    # Handle style parameter
    if param == "style":
        try:
            return StyleMode(value)
        except ValueError:
            msg = f"Invalid style value: {value}"
            raise ValueError(msg)

    # Handle character and style references
    if param in {"character_reference", "style_reference"}:
        ref_class = (
            CharacterReference if param == "character_reference" else StyleReference
        )
        try:
            if is_url(value):
                return ref_class(url=HttpUrl(value), weight=1.0)
            else:
                # Handle reference codes (e.g., p123456)
                return ref_class(code=value, weight=1.0)
        except Exception as e:
            msg = f"Invalid reference value for {param}: {value} ({e!s})"
            raise ValueError(msg)

    # Default case: return as string
    return value


def parse_parameters(param_str: str) -> dict[str, Any]:
    """Parse parameters from a string into a dictionary."""
    if not param_str:
        return []

    # Handle empty parameter case
    if param_str == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)

    chunks = []
    current_chunk = []
    in_quotes = False
    quote_char = None
    current_param = None

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
                chunk_str = "".join(current_chunk)
                if chunk_str.startswith("--"):
                    if current_param:
                        chunks.append(current_param)
                    current_param = chunk_str
                elif current_param:
                    current_param = f"{current_param} {chunk_str}"
                else:
                    current_param = chunk_str
                current_chunk = []
        else:
            current_chunk.append(char)

    # Handle last chunk
    if current_chunk:
        chunk_str = "".join(current_chunk)
        if chunk_str.startswith("--"):
            if current_param:
                chunks.append(current_param)
            current_param = chunk_str
        elif current_param:
            current_param = f"{current_param} {chunk_str}"
        else:
            current_param = chunk_str

    if current_param:
        chunks.append(current_param)

    return chunks


def _process_param_chunk(
    chunk: str, params: dict[str, str | list[str] | None]
) -> tuple[str, str | list[str] | None]:
    """
    Process a parameter chunk into name and value.

    Args:
        chunk: Parameter chunk to process.
        params: Dictionary to store parameters in.

    Returns:
        Tuple of parameter name and value.

    Raises:
        ValueError: If chunk has invalid syntax or missing required value.
    """
    if not chunk or chunk == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)

    # Split on first double dash
    parts = chunk.split("--", 1)
    if len(parts) != 2:
        msg = f"Parameter name cannot start with dash: {chunk}"
        raise ValueError(msg)

    # Split parameter name and value
    param_parts = parts[1].split(maxsplit=1)
    name = param_parts[0].lower()
    expanded_name = PARAMETER_ALIASES.get(name, name)

    # Define flag parameters that don't require values
    flag_params = {"tile", "turbo", "relax", "video", "remix"}

    # Handle flag parameters (no value)
    if len(param_parts) == 1:
        if expanded_name in {"personalization", "p"}:
            return "personalization", None
        if expanded_name == "niji":
            return "version", "niji"
        if expanded_name in flag_params:
            return expanded_name, None
        # For non-flag parameters, raise error if value is missing
        msg = f"Missing value for parameter: {name}"
        raise ValueError(msg)

    # Get value part (everything after the first space)
    value = param_parts[1]

    # Process the value based on parameter type
    if expanded_name in {"personalization", "p"}:
        # Return list of space-separated values for personalization codes
        # Handle quoted values
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]  # Remove quotes
        return "personalization", value.split() if value else None
    elif expanded_name in {"character_reference", "cref"}:
        if value.startswith("<") and value.endswith(">"):
            return "character_reference", [value]
        if value.startswith('"') and value.endswith('"'):
            return "character_reference", [value[1:-1]]
        if value.startswith("'") and value.endswith("'"):
            return "character_reference", [value[1:-1]]
        return "character_reference", value.split()
    elif expanded_name in {"style_reference", "sref"}:
        # Return list of values for style references; if enclosed in angle brackets, treat as single value
        if value.startswith("<") and value.endswith(">"):
            return "style_reference", [value]
        if value.startswith('"') and value.endswith('"'):
            return "style_reference", [value[1:-1]]
        if value.startswith("'") and value.endswith("'"):
            return "style_reference", [value[1:-1]]
        return "style_reference", value.split()
    elif expanded_name == "version" or name == "v":
        # Handle version parameter
        if value.startswith("v"):
            value = value[1:]  # Strip 'v' prefix
        return "version", value
    elif expanded_name == "niji":
        # Handle niji version without adding 'v' prefix; store under key 'version'
        if value.startswith("v"):
            value = value[1:]
        return "version", f"niji {value}"
    else:
        # Handle quoted values for other parameters
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]  # Remove quotes
        # All other parameters are returned as strings
        return expanded_name, value


def _process_current_param(
    current_param: str | None,
    current_values: list[str],
    params: ParamDict,
) -> None:
    """Process and store the current parameter."""
    if current_param is None:
        return
    if current_param == "":
        msg = "Empty parameter name"
        raise ValueError(msg)

    # Validate that required parameters have values
    expanded_name, is_flag = expand_shorthand_param(current_param)

    # Special handling for personalization parameter
    if expanded_name == "personalization":
        if not current_values:
            params[expanded_name] = None  # None for flag usage
            return
        value = process_param_value(current_values)
        validate_param_value(expanded_name, value)
        params[expanded_name] = value
        return

    # Special handling for niji parameter
    if expanded_name == "niji":
        if not current_values:
            params["version"] = "niji"  # Just niji without version
            return
        value = process_param_value(current_values)
        if isinstance(value, str):
            if value.startswith("v"):
                value = value[1:]  # Strip 'v' prefix if present
            params["version"] = f"niji {value}"  # niji with version
        return

    # Regular parameter handling
    if not is_flag and not current_values:
        msg = f"Missing value for parameter: {current_param}"
        raise ValueError(msg)

    # Process and store the parameter
    value = process_param_value(current_values)
    validate_param_value(expanded_name, value)
    if expanded_name == "version":
        if isinstance(value, str):
            if value.startswith("v"):
                value = value[1:]  # Strip 'v' prefix if present
            params[expanded_name] = value
    else:
        params[expanded_name] = value


def parse_parameters(param_str: str) -> dict[str, str | list[str] | None]:
    """
    Parse parameter string into a dictionary.

    Args:
        param_str: Parameter string to parse.

    Returns:
        Dictionary of parameter names and values.

    Raises:
        ValueError: If parameter string has invalid syntax.
    """
    if not param_str:
        return {}

    params: dict[str, str | list[str] | None] = {}
    chunks = _split_param_chunks(param_str)

    for chunk in chunks:
        name, value = _process_param_chunk(chunk, params)
        params[name] = value

    return params
