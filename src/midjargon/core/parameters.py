#!/usr/bin/env python3
# this_file: src/midjargon/core/parameters.py

import re
import shlex
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from pydantic import HttpUrl

from midjargon.core.models import (
    CharacterReference,
    MidjourneyParameters,
    MidjourneyVersion,
    StyleMode,
    StyleReference,
)

# Parameter aliases mapping
ALIASES = {
    "ar": "aspect",
    "s": "stylize",
    "stylize": "stylize",
    "c": "chaos",
    "w": "weird",
    "iw": "image_weight",
    "q": "quality",
    "p": "personalization",
    "niji": "version",
    "tile": "tile",
    "turbo": "turbo",
    "relax": "relax",
    "no": "no",
    "style": "style",
    "seed": "seed",
    "cref": "character_reference",
    "sref": "style_reference",
    "v": "version",
    "cw": "character_weight",
    "sw": "style_weight",
    "sv": "style_version",
}

# Parameters that don't require a value
FLAG_PARAMS = {
    "tile",
    "turbo",
    "relax",
    "video",
    "personalization",
}

# Parameters that expect numeric values
NUMERIC_PARAMS = {
    "stylize",
    "chaos",
    "weird",
    "seed",
    "quality",
    "character_weight",
    "style_weight",
    "style_version",
}


def is_url(value: str) -> bool:
    """Check if a string is a URL."""
    return value.startswith(("http://", "https://"))


def convert_parameter_value(name: str, value: Optional[str | List[str]]) -> Any:
    """Convert a parameter value to its appropriate type.

    Args:
        name: The parameter name.
        value: The parameter value to convert.

    Returns:
        The converted value.

    Raises:
        ValueError: If value conversion fails.
    """
    if name in FLAG_PARAMS:
        return True if value is None else bool(value)

    if value is None:
        msg = f"Missing value for parameter: {name}"
        raise ValueError(msg)

    try:
        if name == "version":
            if value == "niji":
                return MidjourneyVersion.NIJI6
            return MidjourneyVersion(value)
        elif name == "style":
            return str(value)
        elif name == "no":
            if isinstance(value, list):
                return value
            return [x.strip() for x in str(value).split(",")]
        elif name == "character_reference":
            if isinstance(value, list) and len(value) >= 1:
                if is_url(value[0]):
                    url = HttpUrl(quote(value[0]))
                    weight = int(float(value[1])) if len(value) > 1 else 1
                    return CharacterReference(url=url, weight=weight)
                else:
                    code = value[0]
                    weight = int(float(value[1])) if len(value) > 1 else 1
                    return CharacterReference(code=code, weight=weight)
            if is_url(str(value)):
                url = HttpUrl(quote(str(value)))
                return CharacterReference(url=url, weight=1)
            return CharacterReference(code=str(value), weight=1)
        elif name == "style_reference":
            if isinstance(value, list) and len(value) >= 1:
                if is_url(value[0]):
                    url = HttpUrl(quote(value[0]))
                    weight = int(float(value[1])) if len(value) > 1 else 1
                    return StyleReference(url=url, weight=weight)
                else:
                    code = value[0]
                    weight = int(float(value[1])) if len(value) > 1 else 1
                    return StyleReference(code=code, weight=weight)
            if is_url(str(value)):
                url = HttpUrl(quote(str(value)))
                return StyleReference(url=url, weight=1)
            return StyleReference(code=str(value), weight=1)
        elif name in NUMERIC_PARAMS:
            if isinstance(value, list):
                msg = f"Expected single value for numeric parameter {name}"
                raise ValueError(msg)
            val = int(float(str(value)))
            if name == "stylize" and (val < 0 or val > 1000):
                msg = f"Invalid numeric value for {name}: {val} (must be between 0 and 1000)"
                raise ValueError(msg)
            return val
        else:
            return str(value)
    except Exception as e:
        msg = f"Invalid value for parameter {name}: {e!s}"
        raise ValueError(msg)


def parse_parameters(param_str: str) -> Dict[str, Any]:
    """Parse a string of parameters into a validated dictionary.

    Args:
        param_str: String of parameters starting with '--'.

    Returns:
        Dictionary of validated parameters.

    Raises:
        ValueError: If parameter parsing fails.
    """
    tokens = shlex.split(param_str)
    result = {}
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if not token.startswith("--"):
            i += 1
            continue

        name = token[2:]
        if not name:
            msg = "Empty parameter name"
            raise ValueError(msg)

        if name.startswith("-"):
            msg = "Parameter name cannot start with dash"
            raise ValueError(msg)

        canonical = ALIASES.get(name, name)

        # Check if there is a next token and it does not start with '--'
        next_token_exists = i + 1 < len(tokens)
        next_token_is_value = next_token_exists and not tokens[i + 1].startswith("--")

        if next_token_is_value:
            values = []
            while i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                values.append(tokens[i + 1])
                i += 1

            # Convert value based on parameter type
            try:
                if len(values) == 1:
                    result[canonical] = convert_parameter_value(canonical, values[0])
                else:
                    result[canonical] = convert_parameter_value(canonical, values)
            except Exception as e:
                msg = f"Failed to parse parameter {name}: {e!s}"
                raise ValueError(msg)
        elif canonical in FLAG_PARAMS:
            result[canonical] = convert_parameter_value(canonical, None)
        elif canonical == "version" and name == "niji":
            result[canonical] = MidjourneyVersion.NIJI6
        else:
            msg = f"Missing value for parameter: {canonical}"
            raise ValueError(msg)

        i += 1

    return result
