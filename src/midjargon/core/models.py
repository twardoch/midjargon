#!/usr/bin/env python3
# this_file: src/midjargon/core/models.py

from enum import Enum
from typing import Any, Optional

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    field_validator,
)


class MidjourneyVersion(str, Enum):
    """Midjourney model version."""

    V4 = "v4"
    V5 = "v5"
    V5_1 = "v5.1"
    V5_2 = "v5.2"
    V6 = "v6"
    V6_1 = "v6.1"
    NIJI4 = "niji4"
    NIJI5 = "niji5"
    NIJI6 = "niji6"

    @classmethod
    def _missing_(cls, value: Any) -> Optional["MidjourneyVersion"]:
        """Handle missing values by trying to normalize the input."""
        try:
            # Try to normalize version string
            value = str(value).lower().strip()
            if value == "niji":
                return cls.NIJI6
            if value.startswith("v"):
                value = value[1:]
            # Try exact match first
            for member in cls:
                if member.value == value:
                    return member
            # Try prefix match
            for member in cls:
                if member.value.startswith(value):
                    return member
            return None
        except:
            return None


class StyleMode(str, Enum):
    """Available style modes."""

    RAW = "raw"
    CUTE = "cute"
    EXPRESSIVE = "expressive"
    SCENIC = "scenic"
    ORIGINAL = "original"


class ImageReference(BaseModel):
    """Reference to an image."""

    url: HttpUrl
    weight: float = 1.0


class CharacterReference(BaseModel):
    """Reference to a character."""

    url: HttpUrl
    weight: float = 1.0


class StyleReference(BaseModel):
    """Reference to a style."""

    url: HttpUrl
    weight: float = 1.0


class MidjourneyParameters(BaseModel):
    """Parameters for a Midjourney prompt."""

    version: MidjourneyVersion | None = None
    style: StyleMode | None = None
    stylize: int = 100
    chaos: int = 0
    weird: int = 0
    seed: int | str | None = None
    aspect: str = "1:1"
    tile: bool = False
    turbo: bool = False
    relax: bool = False
    no: list[str] = Field(default_factory=list)
    character_reference: CharacterReference | None = None
    style_reference: StyleReference | None = None

    @field_validator("aspect")
    @classmethod
    def validate_aspect(cls, v: str) -> str:
        """Validate aspect ratio format."""
        try:
            w, h = map(int, v.split(":"))
            if w <= 0 or h <= 0:
                raise ValueError
            return f"{w}:{h}"
        except:
            msg = "Invalid aspect ratio format. Expected W:H"
            raise ValueError(msg)

    @field_validator("stylize")
    @classmethod
    def validate_stylize(cls, v: int) -> int:
        """Validate stylize value."""
        if not 0 <= v <= 1000:
            msg = f"Stylize value must be between 0 and 1000, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("chaos")
    @classmethod
    def validate_chaos(cls, v: int) -> int:
        """Validate chaos value."""
        if not 0 <= v <= 100:
            msg = f"Chaos value must be between 0 and 100, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("weird")
    @classmethod
    def validate_weird(cls, v: int) -> int:
        """Validate weird value."""
        if not 0 <= v <= 3000:
            msg = f"Weird value must be between 0 and 3000, got {v}"
            raise ValueError(msg)
        return v


class MidjourneyPrompt(BaseModel):
    """A complete Midjourney prompt."""

    text: str
    image_prompts: list[HttpUrl] = []
    stylize: Optional[float] = 100
    chaos: Optional[float] = 0
    weird: Optional[float] = 0
    image_weight: Optional[float] = 1.0
    seed: Optional[int] = None
    stop: Optional[float] = 100
    aspect_width: Optional[int] = None
    aspect_height: Optional[int] = None
    aspect_ratio: Optional[str] = None
    style: Optional[StyleMode] = None
    version: Optional[MidjourneyVersion] = None
    personalization: bool = False
    quality: Optional[float] = 1.0
    character_reference: list[CharacterReference] = []
    character_weight: Optional[float] = 100
    style_reference: list[StyleReference] = []
    style_weight: Optional[float] = None
    style_version: Optional[int] = 2
    repeat: Optional[int] = None
    turbo: bool = False
    relax: bool = False
    tile: bool = False
    negative_prompt: Optional[str] = None
    extra_params: dict[str, Any] = Field(default_factory=dict)

    def to_string(self) -> str:
        """Convert prompt to string format."""
        parts = [self.text]

        # Add image prompts
        for url in self.image_prompts:
            parts.append(str(url))

        # Add parameters
        params = []
        for field, value in self.model_dump(exclude_unset=True).items():
            if field in {"text", "image_prompts", "extra_params"} or value is None:
                continue
            if isinstance(value, bool) and value:
                params.append(f"--{field}")
            elif isinstance(value, list) and value:
                for v in value:
                    params.append(f"--{field} {v}")
            else:
                params.append(f"--{field} {value}")

        # Add extra parameters
        for key, value in self.extra_params.items():
            if value is None:
                params.append(f"--{key}")
            else:
                params.append(f"--{key} {value}")

        if params:
            parts.append(" ".join(params))

        return " ".join(parts)


class PromptVariant(BaseModel):
    """A variant of a prompt with weight."""

    prompt: MidjourneyPrompt
    weight: float = 1.0
