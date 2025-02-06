"""
Models for Midjourney engine.
"""

import re
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from .constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    CHAOS_RANGE,
    CHARACTER_WEIGHT_RANGE,
    IMAGE_WEIGHT_RANGE,
    QUALITY_RANGE,
    REPEAT_RANGE,
    SEED_RANGE,
    STOP_RANGE,
    STYLE_VERSION_RANGE,
    STYLE_WEIGHT_RANGE,
    STYLIZE_RANGE,
    VALID_NIJI_VERSIONS,
    VALID_STYLES,
    VALID_VERSIONS,
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

    # New parameters
    quality: float | None = Field(None, ge=QUALITY_RANGE[0], le=QUALITY_RANGE[1])
    character_reference: list[str] = Field(default_factory=list)
    character_weight: int | None = Field(
        None, ge=CHARACTER_WEIGHT_RANGE[0], le=CHARACTER_WEIGHT_RANGE[1]
    )
    style_reference: list[str] = Field(default_factory=list)
    style_weight: int | None = Field(
        None, ge=STYLE_WEIGHT_RANGE[0], le=STYLE_WEIGHT_RANGE[1]
    )
    style_version: int | None = Field(
        None, ge=STYLE_VERSION_RANGE[0], le=STYLE_VERSION_RANGE[1]
    )
    repeat: int | None = Field(None, ge=REPEAT_RANGE[0], le=REPEAT_RANGE[1])

    # Flag parameters
    turbo: bool = Field(default=False)
    relax: bool = Field(default=False)
    tile: bool = Field(default=False)

    # Negative prompts
    negative_prompt: str | None = Field(None)

    # Store any unknown parameters
    extra_params: dict[str, str | None] = Field(default_factory=dict)

    @field_validator("text")
    @classmethod
    def clean_text(cls, v: str) -> str:
        """Basic text cleanup."""
        return v.strip()

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str | None) -> str | None:
        """Validate style value."""
        if v is not None and v not in VALID_STYLES:
            msg = f"Invalid style value. Must be one of: {VALID_STYLES}"
            raise ValueError(msg)
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str | None) -> str | None:
        """Validate version value."""
        if v is None:
            return v

        # Handle Niji version
        if v.startswith("niji"):
            parts = v.split()
            if len(parts) == 1:  # Just "niji"
                return v
            version = parts[-1]
            if version not in VALID_NIJI_VERSIONS:
                msg = f"Invalid niji version. Must be one of: {VALID_NIJI_VERSIONS}"
                raise ValueError(msg)
            return v

        # Handle Midjourney version
        version = v.lstrip("v")
        if version not in VALID_VERSIONS:
            msg = f"Invalid version value. Must be one of: {VALID_VERSIONS}"
            raise ValueError(msg)
        return v  # Return original value to preserve 'v' prefix

    @model_validator(mode="after")
    def validate_mode_flags(self) -> Any:
        """Validate mode flag combinations."""
        if self.turbo and self.relax:
            msg = "Cannot use both turbo and relax modes"
            raise ValueError(msg)
        return self
