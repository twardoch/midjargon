#!/usr/bin/env python3
# this_file: src/midjargon/core/parameters.py

import shlex
from typing import Any
from urllib.parse import quote

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
MULTI_VALUE_PARAMS = {"no", "personalization", "character_reference", "style_reference"}

# Parameters that are flags (no value needed)
FLAG_PARAMS = {"tile", "turbo", "relax", "fast", "video"}


def convert_parameter_value(param: str, value: str | None) -> Any:
    """Convert a parameter value to the appropriate type."""
    # Handle flag parameters
    if param in FLAG_PARAMS:
        return True if value is None else value.lower() == "true"

    # Handle empty values
    if value is None:
        return None

    # Handle multi-value parameters
    if param in MULTI_VALUE_PARAMS:
        return value.split(",") if value else []

    # Handle version parameter
    if param == "version":
        if value.startswith("niji"):
            return MidjourneyVersion.NIJI6
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid version value: {value}")

    # Handle numeric parameters
    if param in {
        "stylize",
        "chaos",
        "weird",
        "seed",
        "quality",
        "character_weight",
        "style_weight",
        "style_version",
    }:
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid numeric value for {param}: {value}")

    # Handle style parameter
    if param == "style":
        try:
            return StyleMode(value)
        except ValueError:
            raise ValueError(f"Invalid style value: {value}")

    # Handle character and style references
    if param in {"character_reference", "style_reference"}:
        ref_class = (
            CharacterReference if param == "character_reference" else StyleReference
        )
        if value.startswith("http"):
            return ref_class(url=HttpUrl(value), weight=1.0)
        else:
            return ref_class(code=value, weight=1.0)

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
        raise ValueError(f"Failed to parse parameters: {e}")

    result: dict[str, Any] = {}
    current_param = None

    for part in parts:
        if part.startswith("--"):
            # New parameter
            if current_param:
                # Previous parameter was a flag
                result[current_param] = True
            current_param = part[2:]  # Remove --
            # Resolve alias if exists
            current_param = ALIASES.get(current_param, current_param)
        elif current_param:
            # Parameter value
            try:
                value = convert_parameter_value(current_param, part)
                if current_param in result and current_param in MULTI_VALUE_PARAMS:
                    # Append to existing multi-value parameter
                    if isinstance(result[current_param], list):
                        result[current_param].append(value)
                    else:
                        result[current_param] = [result[current_param], value]
                else:
                    result[current_param] = value
            except Exception as e:
                raise ValueError(f"Failed to parse parameter {current_param}: {e}")
            current_param = None
        else:
            raise ValueError(f"Unexpected value without parameter: {part}")

    # Handle last parameter if it was a flag
    if current_param:
        result[current_param] = True

    return result
