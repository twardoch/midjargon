#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/midjourney.py

from typing import Any

from pydantic import (
    BaseModel,
    HttpUrl,
    ValidationInfo,
    computed_field,
    field_validator,
)

from midjargon.core.models import (
    CharacterReference,
    MidjourneyVersion,
    StyleMode,
    StyleReference,
)


class MidjourneyPrompt(BaseModel):
    """Midjourney prompt model with all parameters."""

    text: str
    image_prompts: list[HttpUrl] = []
    stylize: float | None = 100
    chaos: float | None = 0
    weird: float | None = 0
    image_weight: float | None = 1.0
    seed: int | None = None
    stop: float | None = 100
    aspect_width: int | None = None
    aspect_height: int | None = None
    aspect_ratio: str | None = None
    style: StyleMode | None = None
    version: MidjourneyVersion | None = None
    personalization: bool = False
    quality: float | None = 1.0
    character_reference: list[CharacterReference] = []
    character_weight: float | None = 100
    style_reference: list[StyleReference] = []
    style_weight: float | None = None
    style_version: int | None = 2
    repeat: int | None = None
    turbo: bool = False
    relax: bool = False
    tile: bool = False
    negative_prompt: str | None = None
    extra_params: dict[str, Any] = {}

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

    @field_validator("stylize")
    @classmethod
    def validate_stylize(cls, v: float | None, info: ValidationInfo) -> float | None:
        """Validate stylize value."""
        if v is not None and not 0 <= v <= 1000:
            msg = f"Stylize value must be between 0 and 1000, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("chaos")
    @classmethod
    def validate_chaos(cls, v: float | None, info: ValidationInfo) -> float | None:
        """Validate chaos value."""
        if v is not None and not 0 <= v <= 100:
            msg = f"Chaos value must be between 0 and 100, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("weird")
    @classmethod
    def validate_weird(cls, v: float | None, info: ValidationInfo) -> float | None:
        """Validate weird value."""
        if v is not None and not 0 <= v <= 3000:
            msg = f"Weird value must be between 0 and 3000, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("quality")
    @classmethod
    def validate_quality(cls, v: float | None, info: ValidationInfo) -> float | None:
        """Validate quality value."""
        if v is not None and not 0.25 <= v <= 2.0:
            msg = f"Quality value must be between 0.25 and 2.0, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("character_weight")
    @classmethod
    def validate_character_weight(
        cls, v: float | None, info: ValidationInfo
    ) -> float | None:
        """Validate character weight value."""
        if v is not None and not 0 <= v <= 100:
            msg = f"Character weight must be between 0 and 100, got {v}"
            raise ValueError(msg)
        return v

    @field_validator("style_weight")
    @classmethod
    def validate_style_weight(
        cls, v: float | None, info: ValidationInfo
    ) -> float | None:
        """Validate style weight value."""
        if v is not None and not 0 <= v <= 100:
            msg = f"Style weight must be between 0 and 100, got {v}"
            raise ValueError(msg)
        return v

    @computed_field
    def images(self) -> list[HttpUrl]:
        """Get image URLs."""
        return self.image_prompts

    @computed_field
    def parameters(self) -> dict[str, Any]:
        """Get all parameters as a dictionary."""
        params = self.model_dump(exclude={"text", "image_prompts", "extra_params"})
        return {k: v for k, v in params.items() if v is not None}

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


class MidjourneyParser:
    """Parser for converting between Midjourney prompt formats."""

    def parse_dict(self, prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt.

        Args:
            prompt_dict: Dictionary containing prompt data.

        Returns:
            MidjourneyPrompt instance.

        Raises:
            ValueError: If the prompt text is empty.
        """
        # Validate text
        text = prompt_dict.get("text", "").strip()
        if not text:
            msg = "Empty prompt"
            raise ValueError(msg)

        # Extract known fields
        known_fields = set(MidjourneyPrompt.model_fields)

        # Split into known and extra parameters
        params = {}
        extra_params = {}
        for key, value in prompt_dict.items():
            if key in known_fields:
                params[key] = value
            else:
                extra_params[key] = value

        # Create prompt with all parameters
        return MidjourneyPrompt(text=text, **params, extra_params=extra_params)


def parse_midjourney_dict(prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
    """Convert a dictionary to a MidjourneyPrompt.

    Args:
        prompt_dict: Dictionary containing prompt data.

    Returns:
        MidjourneyPrompt instance.
    """
    parser = MidjourneyParser()
    return parser.parse_dict(prompt_dict)
