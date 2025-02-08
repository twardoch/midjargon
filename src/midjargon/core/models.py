#!/usr/bin/env python3
# this_file: src/midjargon/core/models.py

from enum import Enum
from typing import List, Optional, Union

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ValidationInfo,
    field_validator,
    model_validator,
)


class MidjourneyVersion(str, Enum):
    """Midjourney model version."""

    V4 = "4"
    V5 = "5"
    V5_1 = "5.1"
    V5_2 = "5.2"
    NIJI4 = "niji4"
    NIJI5 = "niji5"
    NIJI6 = "niji6"


class StyleMode(str, Enum):
    """Available style modes."""

    RAW = "raw"


class ImageReference(BaseModel):
    """Reference to an image."""

    url: HttpUrl
    weight: float = 1.0


class CharacterReference(BaseModel):
    """Reference to a character."""

    url: Optional[HttpUrl] = None
    code: Optional[str] = None
    weight: float = 1.0

    def __init__(self, **data):
        super().__init__(**data)
        if not self.url and not self.code:
            msg = "Either url or code must be provided"
            raise ValueError(msg)


class StyleReference(BaseModel):
    """Reference to a style."""

    url: Optional[HttpUrl] = None
    code: Optional[str] = None
    weight: float = 1.0

    def __init__(self, **data):
        super().__init__(**data)
        if not self.url and not self.code:
            msg = "Either url or code must be provided"
            raise ValueError(msg)


class MidjourneyParameters(BaseModel):
    """Parameters for a Midjourney prompt."""

    version: Optional[MidjourneyVersion] = None
    style: Optional[str] = None
    stylize: int = 100
    chaos: int = 0
    weird: int = 0
    seed: Optional[Union[int, str]] = None
    aspect: str = "1:1"
    tile: bool = False
    turbo: bool = False
    relax: bool = False
    no: List[str] = Field(default_factory=list)
    character_reference: Optional[CharacterReference] = None
    style_reference: Optional[StyleReference] = None

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


class MidjourneyPrompt(BaseModel):
    """A complete Midjourney prompt."""

    text: str
    images: List[ImageReference] = Field(default_factory=list)
    parameters: MidjourneyParameters = Field(default_factory=MidjourneyParameters)

    def to_string(self) -> str:
        """Convert the prompt to its string representation."""
        parts = []

        # Add image URLs
        if self.images:
            parts.extend(str(img.url) for img in self.images)

        # Add main text
        parts.append(self.text)

        # Add parameters
        param_dict = self.parameters.model_dump(exclude_none=True)
        for key, value in param_dict.items():
            if isinstance(value, bool) and value:
                parts.append(f"--{key}")
            elif isinstance(value, list):
                if value:  # Only add if list is not empty
                    parts.append(f"--{key} {','.join(map(str, value))}")
            else:
                parts.append(f"--{key} {value}")

        return " ".join(parts)


class PromptVariant(BaseModel):
    """A variant of a prompt with weight."""

    prompt: MidjourneyPrompt
    weight: float = 1.0
