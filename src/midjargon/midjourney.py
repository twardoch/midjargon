#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic"]
# ///

"""
prompt_midjourney.py

Validates and structures Midjourney prompts according to Midjourney's specific rules.
Builds on prompt_midjargon.py for initial parsing.
"""

import re
from typing import Any

from pydantic import BaseModel, Field, field_validator

from midjargon import MidjargonPrompt, parse_prompt

# Parameter ranges and constraints
STYLIZE_RANGE = (0, 1000)
CHAOS_RANGE = (0, 100)
WEIRD_RANGE = (0, 3000)
IMAGE_WEIGHT_RANGE = (0, 3)
SEED_RANGE = (0, 4294967295)
STOP_RANGE = (10, 100)


class ImagePrompt(BaseModel):
    """Represents a validated image prompt URL."""

    url: str = Field(description="Direct image URL ending with allowed extension")

    @field_validator("url")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        """Validates image URL has an allowed file extension."""
        allowed = (".png", ".jpg", ".jpeg", ".gif", ".webp")
        if not str(v).lower().endswith(allowed):
            msg = f"URL must end with one of: {allowed}"
            raise ValueError(msg)

        # Validate URL format
        url_pattern = re.compile(
            r"^https?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if not url_pattern.match(v):
            msg = "Invalid URL format"
            raise ValueError(msg)

        return v


class MidjourneyPrompt(BaseModel):
    """
    Represents a fully validated Midjourney prompt structure.
    Converts raw parameters into specific validated fields.
    """

    # Core prompt components
    text: str = Field(min_length=1)
    image_prompts: list[ImagePrompt] = Field(default_factory=list)

    # Validated numeric parameters
    stylize: int | None = Field(None, ge=STYLIZE_RANGE[0], le=STYLIZE_RANGE[1])
    chaos: int | None = Field(None, ge=CHAOS_RANGE[0], le=CHAOS_RANGE[1])
    weird: int | None = Field(None, ge=WEIRD_RANGE[0], le=WEIRD_RANGE[1])
    image_weight: float | None = Field(
        None, ge=IMAGE_WEIGHT_RANGE[0], le=IMAGE_WEIGHT_RANGE[1]
    )
    seed: int | None = Field(None, ge=SEED_RANGE[0], le=SEED_RANGE[1])
    stop: int | None = Field(None, ge=STOP_RANGE[0], le=STOP_RANGE[1])

    # Aspect ratio as separate width/height
    aspect_width: int | None = Field(None, gt=0)
    aspect_height: int | None = Field(None, gt=0)

    # Style parameters
    style: str | None = Field(None)  # raw, cute, expressive, etc.
    version: str | None = Field(None)  # v5, v6, niji, etc.
    personalization: str | None = Field(None)  # Profile ID or code for --p parameter

    # Store any unknown parameters
    extra_params: dict[str, str | None] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def clean_text(cls, v: str) -> str:
        """Basic text cleanup."""
        return v.strip()

    def _parse_aspect_ratio(self, value: str) -> None:
        """Parse aspect ratio string into width/height."""
        if ":" in value:
            try:
                w, h = value.split(":")
                self.aspect_width = int(w)
                self.aspect_height = int(h)
            except ValueError as e:
                msg = "Invalid aspect ratio format. Expected w:h"
                raise ValueError(msg) from e


def _handle_numeric_param(name: str, value: str | None) -> tuple[str, Any]:
    """Handle numeric parameter conversion."""
    # Handle p parameter separately since it can be a string or None
    if name == "p":
        return "personalization", value

    # Define parameter mappings with their default values and conversion functions
    param_map = {
        ("stylize", "s"): ("stylize", lambda v: int(v) if v else 100),
        ("chaos", "c"): ("chaos", lambda v: int(v) if v else 0),
        ("weird",): ("weird", lambda v: int(v) if v else 0),
        ("iw",): ("image_weight", lambda v: float(v) if v else 1.0),
        ("seed",): ("seed", lambda v: int(v) if v else None),
        ("stop",): ("stop", lambda v: int(v) if v else 100),
    }

    # Find matching parameter and convert value
    for aliases, (param_name, converter) in param_map.items():
        if name in aliases:
            return param_name, converter(value)

    return "", None


def _handle_aspect_ratio(value: str | None) -> tuple[int | None, int | None]:
    """Handle aspect ratio parameter conversion."""
    if not value:
        return None, None
    try:
        w, h = value.split(":")
        return int(w), int(h)
    except ValueError as e:
        msg = "Invalid aspect ratio format. Expected w:h"
        raise ValueError(msg) from e


def _handle_style_param(name: str, value: str | None) -> tuple[str, str | None]:
    """Handle style parameter conversion."""
    if name == "style":
        return "style", value
    elif name == "v":
        return "version", f"v{value}"
    elif name == "niji":
        return "version", f"niji {value}" if value else "niji"
    return "", None


def convert_prompt(midjargon_prompt: MidjargonPrompt) -> MidjourneyPrompt:
    """
    Converts a MidjargonPrompt into a validated MidjourneyPrompt.

    Args:
        midjargon_prompt: Parsed but unvalidated prompt structure.

    Returns:
        Validated MidjourneyPrompt with proper parameter typing.
    """
    # Initialize with core components
    prompt_data: dict[str, Any] = {
        "text": midjargon_prompt.text,
        "image_prompts": [ImagePrompt(url=url) for url in midjargon_prompt.image_urls],
        "extra_params": {},
    }

    # Process each parameter
    for name, value in midjargon_prompt.parameters.items():
        # Try numeric parameters first
        param_name, param_value = _handle_numeric_param(name, value)
        if param_name:
            prompt_data[param_name] = param_value
            continue

        # Handle aspect ratio
        if name in ("ar", "aspect"):
            w, h = _handle_aspect_ratio(value)
            if w is not None and h is not None:
                prompt_data["aspect_width"] = w
                prompt_data["aspect_height"] = h
            continue

        # Handle style parameters
        param_name, param_value = _handle_style_param(name, value)
        if param_name:
            prompt_data[param_name] = param_value
            continue

        # Store unknown parameters
        prompt_data["extra_params"][name] = value

    return MidjourneyPrompt(**prompt_data)


def parse_midjourney(prompt: str) -> list[MidjourneyPrompt]:
    """
    Parse and validate a Midjourney prompt string.
    Handles permutations by returning multiple prompts if needed.

    Args:
        prompt: Raw prompt string.

    Returns:
        List of validated MidjourneyPrompt objects.
    """
    # First parse with midjargon
    midjargon_prompts = parse_prompt(prompt)

    # Convert each to validated MidjourneyPrompt
    return [convert_prompt(p) for p in midjargon_prompts]
