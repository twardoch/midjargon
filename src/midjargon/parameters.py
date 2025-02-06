#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic"]
# ///

"""
parameters.py

Handles parsing and validation of Midjourney prompt parameters.
Provides type-safe parameter handling with proper validation.
"""

from typing import Any, TypeAlias

from pydantic import BaseModel, Field

# Type aliases for clarity
ParamName: TypeAlias = str
ParamValue: TypeAlias = str | None
ParamDict: TypeAlias = dict[ParamName, ParamValue]

# Parameter ranges and constraints
STYLIZE_RANGE = (0, 1000)
CHAOS_RANGE = (0, 100)
WEIRD_RANGE = (0, 3000)
IMAGE_WEIGHT_RANGE = (0, 3)
SEED_RANGE = (0, 4294967295)
STOP_RANGE = (10, 100)


class NumericParam(BaseModel):
    """Base model for numeric parameters with validation."""

    name: str
    value: float | int | None
    min_value: float | int
    max_value: float | int
    default: float | int | None = None

    def validate_value(self) -> float | int | None:
        """Validate the parameter value is within allowed range."""
        if self.value is None:
            return self.default
        if not (self.min_value <= self.value <= self.max_value):
            msg = f"{self.name} must be between {self.min_value} and {self.max_value}"
            raise ValueError(msg)
        return self.value


class AspectRatio(BaseModel):
    """Model for aspect ratio parameter validation."""

    width: int = Field(gt=0)
    height: int = Field(gt=0)

    @classmethod
    def parse(cls, value: str | None) -> tuple[int | None, int | None]:
        """Parse aspect ratio string into width and height."""
        if not value:
            return None, None
        try:
            w, h = value.split(":")
            ratio = cls(width=int(w), height=int(h))
            return ratio.width, ratio.height
        except ValueError as e:
            msg = "Invalid aspect ratio format. Expected w:h"
            raise ValueError(msg) from e


def validate_param_name(name: str) -> None:
    """
    Validate a parameter name.

    Args:
        name: Parameter name to validate.

    Raises:
        ValueError: If name is invalid.
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


def validate_param_value(param: str, value: str | None) -> None:
    """
    Validate that a parameter has a value if required.

    Args:
        param: Parameter name.
        value: Parameter value.

    Raises:
        ValueError: If required value is missing or invalid.
    """
    flag_params = {
        "tile",
        "raw",
        "test",
        "p",  # p can be used without a value to use default profile
    }  # Known flag parameters that don't require values
    numeric_params = {"stylize", "s", "chaos", "c", "weird", "iw", "seed", "stop"}

    # Check if numeric parameters have valid numeric values
    if param in numeric_params and value is not None:
        try:
            float(value)
        except ValueError as e:
            msg = f"Invalid numeric value for parameter {param}: {value}"
            raise ValueError(msg) from e

    # Check if required parameters have values
    if not value and param not in flag_params:
        msg = f"Missing required value for parameter: {param}"
        raise ValueError(msg)

    # Check for invalid quoted values
    if value and (
        (value.startswith('"') and not value.endswith('"'))
        or (value.startswith("'") and not value.endswith("'"))
    ):
        msg = f"Unmatched quotes in parameter value: {value}"
        raise ValueError(msg)


def handle_numeric_param(name: str, value: str | None) -> tuple[str, Any]:
    """
    Handle numeric parameter conversion with validation.

    Args:
        name: Parameter name.
        value: Raw parameter value.

    Returns:
        Tuple of (parameter_name, converted_value).
    """
    # Parameter definitions with validation ranges and defaults
    param_defs = {
        ("stylize", "s"): NumericParam(
            name="stylize",
            value=int(value) if value else None,
            min_value=STYLIZE_RANGE[0],
            max_value=STYLIZE_RANGE[1],
            default=100,
        ),
        ("chaos", "c"): NumericParam(
            name="chaos",
            value=int(value) if value else None,
            min_value=CHAOS_RANGE[0],
            max_value=CHAOS_RANGE[1],
            default=0,
        ),
        ("weird",): NumericParam(
            name="weird",
            value=int(value) if value else None,
            min_value=WEIRD_RANGE[0],
            max_value=WEIRD_RANGE[1],
            default=0,
        ),
        ("iw",): NumericParam(
            name="image_weight",
            value=float(value) if value else None,
            min_value=IMAGE_WEIGHT_RANGE[0],
            max_value=IMAGE_WEIGHT_RANGE[1],
            default=1.0,
        ),
        ("seed",): NumericParam(
            name="seed",
            value=int(value) if value else None,
            min_value=SEED_RANGE[0],
            max_value=SEED_RANGE[1],
            default=None,
        ),
        ("stop",): NumericParam(
            name="stop",
            value=int(value) if value else None,
            min_value=STOP_RANGE[0],
            max_value=STOP_RANGE[1],
            default=100,
        ),
    }

    # Find matching parameter and validate
    for aliases, param in param_defs.items():
        if name in aliases:
            return param.name, param.validate_value()

    return "", None


def handle_style_param(name: str, value: str | None) -> tuple[str, str | None]:
    """
    Handle style parameter conversion.

    Args:
        name: Parameter name.
        value: Parameter value.

    Returns:
        Tuple of (parameter_name, converted_value).
    """
    if name == "style":
        return "style", value
    elif name == "v":
        return "version", f"v{value}"
    elif name == "niji":
        return "version", f"niji {value}" if value else "niji"
    return "", None


def _handle_value_conversions(name: str, value: str | None) -> tuple[str, str | None]:
    """Handle special parameter name and value conversions."""
    # Handle numeric parameters with shorthand names
    if name in {"s", "c"}:
        name = "stylize" if name == "s" else "chaos"

    # Handle special parameter conversions
    if name == "v":
        name = "version"
        value = f"v{value}" if value else None
    elif name == "niji":
        name = "version"
        value = f"niji {value}" if value else "niji"

    return name, value


def parse_parameters(param_str: str) -> ParamDict:
    """Parse parameter string into a dictionary of parameter names and values."""
    params: ParamDict = {}
    if not param_str:
        return params

    if not param_str.startswith("--"):
        msg = "Parameters must start with --"
        raise ValueError(msg)

    if param_str == "--":
        msg = "Empty parameter name"
        raise ValueError(msg)

    chunks = [c.strip() for c in param_str.split("--") if c.strip()]
    for chunk in chunks:
        parts = chunk.split(None, 1)
        if not parts:
            msg = "Empty parameter name"
            raise ValueError(msg)

        name = parts[0]
        value = parts[1] if len(parts) > 1 else None

        # Handle value conversions
        name, value = _handle_value_conversions(name, value)

        # Validate and handle quotes
        validate_param_name(name)
        validate_param_value(name, value)
        if value and value.startswith(('"', "'")) and value.endswith(value[0]):
            value = value[1:-1]

        params[name] = value

    return params
