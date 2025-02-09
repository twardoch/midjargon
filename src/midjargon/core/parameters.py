#!/usr/bin/env python3
# this_file: src/midjargon/core/parameters.py

import shlex
from typing import Any
from urllib.parse import urlparse

from pydantic import HttpUrl

from midjargon.core.models import (
    CharacterReference,
    MidjourneyVersion,
    StyleMode,
    StyleReference,
)

# Parameter aliases mapping
ALIASES = {
    # Version aliases
    "v": "version",
    "ver": "version",
    "niji": "version",
    # Style aliases
    "s": "stylize",
    # Chaos aliases
    "c": "chaos",
    # Weird aliases
    "w": "weird",
    # Seed aliases
    "sameseed": "seed",
    # Aspect ratio aliases
    "ar": "aspect",
    # Character reference aliases
    "cref": "character_reference",
    # Style reference aliases
    "sref": "style_reference",
    # Character weight aliases
    "cw": "character_weight",
    # Style weight aliases
    "sw": "style_weight",
    # Style version aliases
    "sv": "style_version",
    # Personalization aliases
    "p": "personalization",
}

# Parameters that can have multiple values
MULTI_VALUE_PARAMS = {"no", "character_reference", "style_reference"}

# Parameters that are flags (no value needed)
FLAG_PARAMS = {"tile", "turbo", "relax", "fast", "video", "personalization"}

# Parameters that should remain as strings
STRING_PARAMS = {"aspect", "negative_prompt"}

# Parameters that should be integers
INT_PARAMS = {"seed", "style_version", "repeat"}


def is_url(value: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except:
        return False


def convert_parameter_value(param: str, value: str | None) -> Any:
    """Convert a parameter value to the appropriate type."""
    # Handle flag parameters
    if param in FLAG_PARAMS:
        return True if value is None else value.lower() == "true"

    # Handle empty values
    if value is None:
        return None

    # Handle string parameters
    if param in STRING_PARAMS:
        return str(value)

    # Handle version parameter
    if param == "version":
        try:
            return MidjourneyVersion(value)
        except ValueError:
            msg = f"Invalid version value: {value}"
            raise ValueError(msg)

    # Handle integer parameters
    if param in INT_PARAMS:
        try:
            return int(value)
        except ValueError:
            msg = f"Invalid integer value for {param}: {value}"
            raise ValueError(msg)

    # Handle float parameters
    if param in {
        "stylize",
        "chaos",
        "weird",
        "quality",
        "character_weight",
        "style_weight",
        "image_weight",
        "stop",
    }:
        try:
            return float(value)
        except ValueError:
            msg = f"Invalid numeric value for {param}: {value}"
            raise ValueError(msg)

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
                return ref_class(
                    url=HttpUrl(f"https://example.com/{value}"), code=value, weight=1.0
                )
        except Exception:
            msg = f"Invalid reference value for {param}: {value}"
            raise ValueError(msg)

    # Default case: return as string
    return value


def parse_parameters(param_str: str) -> dict[str, Any]:
    """Parse parameters from a string into a dictionary."""
    if not param_str:
        return {}

    # Split parameters while preserving quoted strings
    try:
        parts = shlex.split(param_str)
    except ValueError as e:
        msg = f"Failed to parse parameters: {e}"
        raise ValueError(msg)

    result: dict[str, Any] = {}
    current_param = None
    current_values = []

    for part in parts:
        if part.startswith("--"):
            # Store previous parameter if exists
            if current_param:
                try:
                    if current_param in MULTI_VALUE_PARAMS:
                        # Handle multi-value parameters
                        values = (
                            [
                                convert_parameter_value(current_param, v)
                                for v in current_values
                            ]
                            if current_values
                            else [True]
                        )
                        if current_param in result:
                            result[current_param].extend(values)
                        else:
                            result[current_param] = values
                    else:
                        # Handle single value parameters
                        value = convert_parameter_value(
                            current_param, current_values[0] if current_values else None
                        )
                        result[current_param] = value
                except Exception as e:
                    msg = f"Failed to parse parameter {current_param}: {e}"
                    raise ValueError(msg)

            # Start new parameter
            current_param = ALIASES.get(
                part[2:], part[2:]
            )  # Remove -- and resolve alias
            current_values = []
        elif current_param:
            current_values.append(part)
        else:
            msg = f"Unexpected value without parameter: {part}"
            raise ValueError(msg)

    # Handle last parameter
    if current_param:
        try:
            if current_param in MULTI_VALUE_PARAMS:
                values = (
                    [convert_parameter_value(current_param, v) for v in current_values]
                    if current_values
                    else [True]
                )
                if current_param in result:
                    result[current_param].extend(values)
                else:
                    result[current_param] = values
            else:
                value = convert_parameter_value(
                    current_param, current_values[0] if current_values else None
                )
                result[current_param] = value
        except Exception as e:
            msg = f"Failed to parse parameter {current_param}: {e}"
            raise ValueError(msg)

    return result
