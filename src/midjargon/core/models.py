#!/usr/bin/env python3
# this_file: src/midjargon/core/models.py
from __future__ import annotations

import re
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
            value = str(value).lower().strip()

            # Handle numeric versions (e.g., 4, 5, 5.2)
            if value.replace(".", "").isdigit():
                value = f"v{value}"

            # Handle v prefix
            if not value.startswith("v") and not value.startswith("niji"):
                value = f"v{value}"

            # Try exact match
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

    url: str  # stored as str so comparisons with plain strings work directly
    weight: float = Field(default=1.0, ge=0.0, le=2.0)

    @field_validator("url", mode="before")
    @classmethod
    def coerce_url_to_str(cls, v: Any) -> str:
        """Accept HttpUrl or str; always store as plain string."""
        return str(v)

    def __str__(self) -> str:
        """Convert to string format."""
        return self.url


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
    """Parameters for a Midjourney prompt.

    Range validation is performed by MidjourneyParser.parse_dict before
    constructing this model, so ge/le constraints are intentionally omitted
    here to keep the model a plain data container.
    """

    version: MidjourneyVersion | str | None = None
    style: StyleMode | None = None
    stylize: float | None = None
    chaos: float | None = None
    weird: float | None = None
    image_weight: float | None = None
    seed: int | str | None = None
    stop: int | None = None
    aspect_width: int | None = None
    aspect_height: int | None = None
    aspect_ratio: str | None = None
    tile: bool = False
    turbo: bool = False
    relax: bool = False
    no: list[str] = Field(default_factory=list)
    character_reference: list[str] = Field(default_factory=list)
    style_reference: list[str] = Field(default_factory=list)
    character_weight: float | None = None
    style_weight: float | None = None
    style_version: int | None = None
    repeat: int | None = None
    personalization: bool | list[str] = False
    quality: float | None = None
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
        if isinstance(v, MidjourneyVersion):
            return v
        if isinstance(v, str):
            v_lower = v.lower().strip()
            # "niji" or "niji N" — keep as plain string
            if re.match(r"^niji(\s+\d+)?$", v_lower):
                return v_lower
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

        if self.version:
            parts.append(f"--v {self.version}")
        if self.style:
            parts.append(f"--style {self.style.value}")
        if self.stylize is not None and self.stylize != 100.0:
            parts.append(f"--s {self.stylize}")
        if self.chaos is not None and self.chaos > 0:
            parts.append(f"--c {self.chaos}")
        if self.weird is not None and self.weird > 0:
            parts.append(f"--weird {self.weird}")
        if self.seed is not None:
            parts.append(f"--seed {self.seed}")
        if self.image_weight is not None:
            parts.append(f"--iw {self.image_weight}")
        if self.stop is not None:
            parts.append(f"--stop {self.stop}")
        if self.aspect:
            parts.append(f"--ar {self.aspect}")
        if self.tile:
            parts.append("--tile")
        if self.turbo:
            parts.append("--turbo")
        if self.relax:
            parts.append("--relax")
        if self.no:
            parts.append(f"--no {','.join(self.no)}")
        if self.character_reference:
            for ref in self.character_reference:
                parts.append(f"--cref {ref}")
        if self.style_reference:
            for ref in self.style_reference:
                parts.append(f"--sref {ref}")
        if self.character_weight is not None and self.character_weight != 100.0:
            parts.append(f"--cw {self.character_weight}")
        if self.style_weight is not None:
            parts.append(f"--sw {self.style_weight}")
        if self.style_version is not None and self.style_version != 2:
            parts.append(f"--sv {self.style_version}")
        if self.repeat is not None:
            parts.append(f"--r {self.repeat}")
        if self.personalization:
            parts.append("--p")
        if self.quality is not None and self.quality != 1.0:
            parts.append(f"--q {self.quality}")
        if self.negative_prompt:
            parts.append(f"--no {self.negative_prompt}")
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
        for img in self.image_prompts:
            parts.append(str(img))
        param_str = self.parameters.to_string()
        if param_str:
            parts.append(param_str)
        return " ".join(parts)

    def to_string(self) -> str:
        """Convert to string format."""
        return str(self)

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """Override model_dump to flatten parameters into top-level dict."""
        data = super().model_dump(**kwargs)
        if "parameters" in data:
            params = data["parameters"]
            data.update(params)
            del data["parameters"]
        return data

    # ------------------------------------------------------------------
    # Property accessors that delegate to parameters
    # ------------------------------------------------------------------

    @property
    def version(self) -> MidjourneyVersion | str | None:
        return self.parameters.version

    @property
    def style(self) -> StyleMode | None:
        return self.parameters.style

    @property
    def stylize(self) -> float | None:
        return self.parameters.stylize

    @property
    def chaos(self) -> float | None:
        return self.parameters.chaos

    @property
    def weird(self) -> float | None:
        return self.parameters.weird

    @property
    def image_weight(self) -> float | None:
        return self.parameters.image_weight

    @property
    def seed(self) -> int | str | None:
        return self.parameters.seed

    @property
    def stop(self) -> int | None:
        return self.parameters.stop

    @property
    def aspect_width(self) -> int | None:
        return self.parameters.aspect_width

    @property
    def aspect_height(self) -> int | None:
        return self.parameters.aspect_height

    @property
    def aspect_ratio(self) -> str | None:
        return self.parameters.aspect_ratio

    @property
    def aspect(self) -> str | None:
        return self.parameters.aspect

    @property
    def tile(self) -> bool:
        return self.parameters.tile

    @property
    def turbo(self) -> bool:
        return self.parameters.turbo

    @property
    def relax(self) -> bool:
        return self.parameters.relax

    @property
    def no(self) -> list[str]:
        return self.parameters.no

    @property
    def character_reference(self) -> list[str]:
        return self.parameters.character_reference

    @property
    def style_reference(self) -> list[str]:
        return self.parameters.style_reference

    @property
    def character_weight(self) -> float | None:
        return self.parameters.character_weight

    @property
    def style_weight(self) -> float | None:
        return self.parameters.style_weight

    @property
    def style_version(self) -> int | None:
        return self.parameters.style_version

    @property
    def repeat(self) -> int | None:
        return self.parameters.repeat

    @property
    def personalization(self) -> bool | list[str]:
        return self.parameters.personalization

    @property
    def quality(self) -> float | None:
        return self.parameters.quality

    @property
    def negative_prompt(self) -> str | None:
        return self.parameters.negative_prompt

    @property
    def extra_params(self) -> dict[str, Any]:
        return self.parameters.extra_params


class PromptVariant(BaseModel):
    """A variant of a prompt with weight."""

    prompt: MidjourneyPrompt
    weight: float = 1.0
