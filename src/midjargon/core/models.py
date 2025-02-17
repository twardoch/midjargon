#!/usr/bin/env python3
# this_file: src/midjargon/core/models.py

from enum import Enum
from typing import Any, Optional

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ValidationInfo,
    computed_field,
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

            # Handle numeric versions (e.g., 4, 5, 6)
            if value.replace(".", "").isdigit():
                if "." not in value:
                    value = f"v{value}"
                else:
                    value = f"v{value}"

            # Handle niji versions
            if value == "niji":
                return cls.NIJI6
            if value.startswith("niji"):
                for member in cls:
                    if member.value == value:
                        return member
                return cls.NIJI6

            # Handle v prefix
            if not value.startswith("v") and not value.startswith("niji"):
                value = f"v{value}"

            # Try exact match first
            for member in cls:
                if member.value == value:
                    return member

            # Try prefix match for v* versions
            if value.startswith("v"):
                base_version = value.split(".")[0]
                latest_version = None
                for member in cls:
                    if member.value.startswith(base_version):
                        if (
                            latest_version is None
                            or member.value > latest_version.value
                        ):
                            latest_version = member
                if latest_version:
                    return latest_version

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
    weight: float = Field(default=1.0, ge=0.0, le=2.0)


class CharacterReference(BaseModel):
    """Reference to a character."""

    url: HttpUrl | None = None
    weight: float = Field(default=1.0, ge=0.0, le=2.0)
    code: str | None = None

    @field_validator("url", "code")
    @classmethod
    def validate_reference(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate that either url or code is provided."""
        if info.data.get("url") is None and info.data.get("code") is None:
            msg = "Either url or code must be provided"
            raise ValueError(msg)
        return v


class StyleReference(BaseModel):
    """Reference to a style."""

    url: HttpUrl | None = None
    weight: float = Field(default=1.0, ge=0.0, le=2.0)
    code: str | None = None

    @field_validator("url", "code")
    @classmethod
    def validate_reference(cls, v: Any, info: ValidationInfo) -> Any:
        """Validate that either url or code is provided."""
        if info.data.get("url") is None and info.data.get("code") is None:
            msg = "Either url or code must be provided"
            raise ValueError(msg)
        return v


class MidjourneyParameters(BaseModel):
    """Parameters for a Midjourney prompt."""

    version: MidjourneyVersion | None = None
    style: StyleMode | None = None
    stylize: int = Field(default=100, ge=0, le=1000)
    chaos: int = Field(default=0, ge=0, le=100)
    weird: int = Field(default=0, ge=0, le=3000)
    seed: int | str | None = None
    aspect: str = "1:1"
    tile: bool = False
    turbo: bool = False
    relax: bool = False
    no: list[str] = Field(default_factory=list)
    character_reference: list[CharacterReference] = Field(default_factory=list)
    style_reference: list[StyleReference] = Field(default_factory=list)

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
    image_prompts: list[HttpUrl] = Field(default_factory=list)
    stylize: float = Field(default=100, ge=0, le=1000)
    chaos: float = Field(default=0, ge=0, le=100)
    weird: float = Field(default=0, ge=0, le=3000)
    image_weight: float = Field(default=1.0, ge=0, le=2.0)
    seed: int | None = None
    stop: float = Field(default=100, ge=0, le=100)
    aspect_width: int | None = None
    aspect_height: int | None = None
    aspect_ratio: str | None = None
    style: StyleMode | None = None
    version: MidjourneyVersion | None = None
    personalization: bool = False
    quality: float = Field(default=1.0, ge=0.25, le=2.0)
    character_reference: list[CharacterReference] = Field(default_factory=list)
    character_weight: float = Field(default=100, ge=0, le=100)
    style_reference: list[StyleReference] = Field(default_factory=list)
    style_weight: float | None = Field(default=None, ge=0, le=100)
    style_version: int = Field(default=2, ge=1, le=3)
    repeat: int | None = None
    turbo: bool = False
    relax: bool = False
    tile: bool = False
    negative_prompt: str | None = None
    extra_params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str | None, info: ValidationInfo) -> str | None:
        """Validate aspect ratio format."""
        if v is not None:
            try:
                w, h = map(int, v.split(":"))
                if w <= 0 or h <= 0:
                    msg = "Invalid aspect ratio: values must be positive"
                    raise ValueError(msg)
                info.data["aspect_width"] = w
                info.data["aspect_height"] = h
            except ValueError as e:
                msg = f"Invalid aspect ratio format: {e}"
                raise ValueError(msg)
        return v

    @field_validator("character_reference", "style_reference")
    @classmethod
    def validate_references(cls, v: list[Any], info: ValidationInfo) -> list[Any]:
        """Validate reference lists."""
        if v is None:
            return []
        if isinstance(v, str) and v == "[]":
            return []
        return v

    @computed_field
    def images(self) -> list[HttpUrl]:
        """Get image URLs."""
        return self.image_prompts

    @property
    def parameters(self) -> MidjourneyParameters:
        """Get all parameters as a MidjourneyParameters object."""
        exclude = {"text", "image_prompts", "extra_params", "images", "parameters"}
        params = {}
        for field_name, field in self.model_fields.items():
            if field_name not in exclude:
                value = getattr(self, field_name)
                if value is not None and value != field.default:
                    if field_name == "character_reference" and not value:
                        continue
                    if field_name == "style_reference" and not value:
                        continue
                    params[field_name] = value
        return MidjourneyParameters(**params)

    def to_string(self) -> str:
        """Convert prompt to string format."""
        parts = [self.text]

        # Add image prompts
        for url in self.image_prompts:
            parts.append(str(url))

        # Add parameters
        params = []
        for field, value in self.parameters.model_dump().items():
            if value is None or (isinstance(value, list | dict) and not value):
                continue
            if isinstance(value, bool):
                if value:
                    params.append(f"--{field}")
            elif isinstance(value, list | dict):
                params.append(f"--{field} {value}")
            else:
                params.append(f"--{field} {value}")

        if params:
            parts.append(" ".join(params))

        return " ".join(parts)


class PromptVariant(BaseModel):
    """A variant of a prompt with weight."""

    prompt: MidjourneyPrompt
    weight: float = 1.0
