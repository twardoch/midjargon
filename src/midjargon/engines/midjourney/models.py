"""
Models for Midjourney engine.
"""

import re

from pydantic import BaseModel, Field, field_validator

from .constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    CHAOS_RANGE,
    IMAGE_WEIGHT_RANGE,
    SEED_RANGE,
    STOP_RANGE,
    STYLIZE_RANGE,
    WEIRD_RANGE,
)


class ImagePrompt(BaseModel):
    """Represents a validated image prompt URL."""

    url: str = Field(description="Direct image URL ending with allowed extension")

    @field_validator("url")
    @classmethod
    def validate_extension(cls, v: str) -> str:
        """Validates image URL has an allowed file extension."""
        if not str(v).lower().endswith(ALLOWED_IMAGE_EXTENSIONS):
            msg = f"URL must end with one of: {ALLOWED_IMAGE_EXTENSIONS}"
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
