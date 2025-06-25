#!/usr/bin/env python3
# this_file: src/midjargon/core/models.py
from __future__ import annotations

from enum import Enum
from typing import Any, TypeVar

from pydantic import (BaseModel, Field, HttpUrl, field_validator,
                      model_validator)

T = TypeVar("T", bound="BaseModel")


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
    def _missing_(cls, value: Any) -> MidjourneyVersion | None:
        """Handle missing values by trying to normalize the input."""
        try:
            # Try to normalize version string
            value = str(value).lower().strip()

            # Handle numeric versions (e.g., 4, 5, 6)
            if value.replace(".", "").isdigit():
                value = f"v{value}" if "." not in value else f"v{value}"

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
                    if member.value.startswith(base_version) and (
                        latest_version is None or member.value > latest_version.value
                    ):
                        latest_version = member
                if latest_version:
                    return latest_version

            return None
        except Exception:
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

    def __str__(self) -> str:
        """Convert to string format."""
        return str(self.url)


class CharacterReference(BaseModel):
    """Reference to a character."""

    url: HttpUrl | None = None
    code: str | None = None
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

    @model_validator(mode="before")
    @classmethod
    def validate_reference(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate that at least one of url or code is provided."""
        if not data.get("url") and not data.get("code"):
            msg = "At least one of url or code must be provided"
            raise ValueError(msg)
        return data


class StyleReference(BaseModel):
    """Reference to a style."""

    url: HttpUrl | None = None
    code: str | None = None
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

    @model_validator(mode="before")
    @classmethod
    def validate_reference(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate that at least one of url or code is provided."""
        if not data.get("url") and not data.get("code"):
            msg = "At least one of url or code must be provided"
            raise ValueError(msg)
        return data


class MidjourneyParameters(BaseModel):
    """Parameters for a Midjourney prompt."""

    version: MidjourneyVersion | str | None = None
    style: StyleMode | None = None
    stylize: float = Field(default=100.0, ge=0.0, le=1000.0)
    chaos: float = Field(default=0.0, ge=0.0, le=100.0)
    weird: float = Field(default=0.0, ge=0.0, le=3000.0)
    seed: int | str | None = None
    aspect_width: int | None = None
    aspect_height: int | None = None
    aspect_ratio: str | None = None
    tile: bool = False
    turbo: bool = False
    relax: bool = False
    no: list[str] = Field(default_factory=list)
    character_reference: list[CharacterReference] = Field(default_factory=list)
    style_reference: list[StyleReference] = Field(default_factory=list)
    character_weight: float = Field(default=100.0, ge=0.0, le=200.0)
    style_weight: float | None = Field(default=None, ge=0.0, le=200.0)
    style_version: int = Field(default=2, ge=1, le=3)
    repeat: int | None = Field(default=None, ge=1, le=40)
    personalization: bool = False
    quality: float = Field(default=1.0, ge=0.25, le=2.0)
    negative_prompt: str | None = None
    extra_params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str | None) -> str | None:
        """Validate aspect ratio format."""
        if v is not None:
            try:
                parts = v.split(":")
                if len(parts) != 2:
                    msg = "Invalid aspect ratio format: must be width:height"
                    raise ValueError(msg)
                w, h = map(int, parts)
                if w <= 0 or h <= 0:
                    msg = "Invalid aspect ratio: values must be positive"
                    raise ValueError(msg)
                return f"{w}:{h}"
            except ValueError as e:
                msg = f"Invalid aspect ratio format: {e}"
                raise ValueError(msg)
        return v

    @field_validator("version")
    @classmethod
    def validate_version(
        cls, v: MidjourneyVersion | str | None
    ) -> MidjourneyVersion | str | None:
        """Validate version value."""
        if v is None:
            return None
        if isinstance(v, str) and v.lower() == "niji":
            return "niji"
        if isinstance(v, str):
            try:
                return MidjourneyVersion(v)
            except ValueError:
                msg = f"Invalid version value: {v}"
                raise ValueError(msg)
        return v

    @field_validator("seed")
    @classmethod
    def validate_seed(cls, v: int | str | None) -> int | str | None:
        """Validate seed value."""
        if v is None:
            return None
        if isinstance(v, str) and v.lower() in {"random", "none"}:
            return v.lower()
        if isinstance(v, int | str):
            try:
                return int(v)
            except ValueError:
                msg = f"Invalid seed value: {v}"
                raise ValueError(msg)
        return v

    @property
    def aspect(self) -> str | None:
        """Get the aspect ratio string."""
        if self.aspect_ratio:
            return self.aspect_ratio
        if self.aspect_width and self.aspect_height:
            return f"{self.aspect_width}:{self.aspect_height}"
        return None

    def to_string(self) -> str:
        """Convert parameters to string format."""
        parts = []

        # Handle version
        if self.version:
            parts.append(f"--v {self.version}")

        # Handle style
        if self.style:
            parts.append(f"--style {self.style.value}")

        # Handle numeric parameters
        if self.stylize != 100.0:
            parts.append(f"--s {self.stylize}")
        if self.chaos > 0:
            parts.append(f"--c {self.chaos}")
        if self.weird > 0:
            parts.append(f"--weird {self.weird}")
        if self.seed is not None:
            parts.append(f"--seed {self.seed}")

        # Handle aspect ratio
        if self.aspect:
            parts.append(f"--ar {self.aspect}")

        # Handle boolean flags
        if self.tile:
            parts.append("--tile")
        if self.turbo:
            parts.append("--turbo")
        if self.relax:
            parts.append("--relax")

        # Handle negative prompts
        if self.no:
            parts.append(f"--no {','.join(self.no)}")

        # Handle references
        if self.character_reference:
            for ref in self.character_reference:
                if ref.url:
                    parts.append(f"--cref {ref.url}")
                elif ref.code:
                    parts.append(f"--cref {ref.code}")
                if ref.weight != 1.0:
                    parts.append(f"--cw {ref.weight}")

        if self.style_reference:
            for ref in self.style_reference:
                if ref.url:
                    parts.append(f"--sref {ref.url}")
                elif ref.code:
                    parts.append(f"--sref {ref.code}")
                if ref.weight != 1.0:
                    parts.append(f"--sw {ref.weight}")

        # Handle other parameters
        if self.character_weight != 100.0:
            parts.append(f"--cw {self.character_weight}")
        if self.style_weight is not None:
            parts.append(f"--sw {self.style_weight}")
        if self.style_version != 2:
            parts.append(f"--sv {self.style_version}")
        if self.repeat is not None:
            parts.append(f"--r {self.repeat}")
        if self.personalization:
            parts.append("--p")
        if self.quality != 1.0:
            parts.append(f"--q {self.quality}")
        if self.negative_prompt:
            parts.append(f"--no {self.negative_prompt}")

        # Handle extra parameters
        for key, value in self.extra_params.items():
            if value is True:
                parts.append(f"--{key}")
            elif value is not False:
                parts.append(f"--{key} {value}")

        return " ".join(parts)


class MidjourneyPrompt(BaseModel):
    """A Midjourney prompt."""

    text: str
    image_prompts: list[ImageReference] = Field(default_factory=list)
    parameters: MidjourneyParameters = Field(default_factory=MidjourneyParameters)
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

    def __str__(self) -> str:
        """Convert to string format."""
        parts = [self.text]

        # Add image prompts
        for img in self.image_prompts:
            parts.append(str(img))

        # Add parameters
        param_str = self.parameters.to_string()
        if param_str:
            parts.append(param_str)

        return " ".join(parts)

    def to_string(self) -> str:
        """Convert to string format."""
        return str(self)

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """Override model_dump to handle nested models correctly."""
        data = super().model_dump(**kwargs)
        if "parameters" in data:
            params = data["parameters"]
            data.update(params)
            del data["parameters"]
        return data

    # Property methods to expose parameters
    @property
    def version(self) -> MidjourneyVersion | str | None:
        """Get version parameter."""
        return self.parameters.version

    @property
    def style(self) -> StyleMode | None:
        """Get style parameter."""
        return self.parameters.style

    @property
    def stylize(self) -> float:
        """Get stylize parameter."""
        return self.parameters.stylize

    @property
    def chaos(self) -> float:
        """Get chaos parameter."""
        return self.parameters.chaos

    @property
    def weird(self) -> float:
        """Get weird parameter."""
        return self.parameters.weird

    @property
    def seed(self) -> int | str | None:
        """Get seed parameter."""
        return self.parameters.seed

    @property
    def aspect_width(self) -> int | None:
        """Get aspect width parameter."""
        return self.parameters.aspect_width

    @property
    def aspect_height(self) -> int | None:
        """Get aspect height parameter."""
        return self.parameters.aspect_height

    @property
    def aspect_ratio(self) -> str | None:
        """Get aspect ratio parameter."""
        return self.parameters.aspect_ratio

    @property
    def aspect(self) -> str | None:
        """Get aspect ratio string."""
        return self.parameters.aspect

    @property
    def tile(self) -> bool:
        """Get tile parameter."""
        return self.parameters.tile

    @property
    def turbo(self) -> bool:
        """Get turbo parameter."""
        return self.parameters.turbo

    @property
    def relax(self) -> bool:
        """Get relax parameter."""
        return self.parameters.relax

    @property
    def no(self) -> list[str]:
        """Get no parameter."""
        return self.parameters.no

    @property
    def character_reference(self) -> list[CharacterReference]:
        """Get character reference parameter."""
        return self.parameters.character_reference

    @property
    def style_reference(self) -> list[StyleReference]:
        """Get style reference parameter."""
        return self.parameters.style_reference

    @property
    def character_weight(self) -> float:
        """Get character weight parameter."""
        return self.parameters.character_weight

    @property
    def style_weight(self) -> float | None:
        """Get style weight parameter."""
        return self.parameters.style_weight

    @property
    def style_version(self) -> int:
        """Get style version parameter."""
        return self.parameters.style_version

    @property
    def repeat(self) -> int | None:
        """Get repeat parameter."""
        return self.parameters.repeat

    @property
    def personalization(self) -> bool:
        """Get personalization parameter."""
        return self.parameters.personalization

    @property
    def quality(self) -> float:
        """Get quality parameter."""
        return self.parameters.quality

    @property
    def negative_prompt(self) -> str | None:
        """Get negative prompt parameter."""
        return self.parameters.negative_prompt

    @property
    def extra_params(self) -> dict[str, Any]:
        """Get extra parameters."""
        return self.parameters.extra_params


class PromptVariant(BaseModel):
    """A variant of a prompt with weight."""

    prompt: MidjourneyPrompt
    weight: float = 1.0
