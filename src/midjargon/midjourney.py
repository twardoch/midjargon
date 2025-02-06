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
            except ValueError:
                msg = "Invalid aspect ratio format. Expected w:h"
                raise ValueError(msg)


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
        # Handle known numeric parameters
        if name in ("stylize", "s"):
            prompt_data["stylize"] = int(value) if value else 100
        elif name in ("chaos", "c"):
            prompt_data["chaos"] = int(value) if value else 0
        elif name == "weird":
            prompt_data["weird"] = int(value) if value else 0
        elif name == "iw":
            prompt_data["image_weight"] = float(value) if value else 1.0
        elif name == "seed":
            prompt_data["seed"] = int(value) if value else None
        elif name == "stop":
            prompt_data["stop"] = int(value) if value else 100

        # Handle aspect ratio
        elif name in ("ar", "aspect"):
            if value:
                try:
                    w, h = value.split(":")
                    prompt_data["aspect_width"] = int(w)
                    prompt_data["aspect_height"] = int(h)
                except ValueError:
                    msg = "Invalid aspect ratio format. Expected w:h"
                    raise ValueError(msg)

        # Handle style and version
        elif name == "style":
            prompt_data["style"] = value
        elif name == "v":
            prompt_data["version"] = f"v{value}"
        elif name == "niji":
            prompt_data["version"] = f"niji {value}" if value else "niji"

        # Store unknown parameters
        else:
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
