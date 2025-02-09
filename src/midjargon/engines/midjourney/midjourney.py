#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/midjourney.py

from typing import Any, Optional

from pydantic import BaseModel, HttpUrl

from midjargon.core.models import (
    CharacterReference,
    MidjourneyVersion,
    StyleMode,
    StyleReference,
)
from midjargon.core.parameters import parse_parameters


class MidjourneyPrompt(BaseModel):
    """Midjourney prompt model with all parameters."""

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
    extra_params: dict[str, Any] = {}

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
            raise ValueError("Empty prompt")

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
        return MidjourneyPrompt(**params, extra_params=extra_params)


def parse_midjourney_dict(prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
    """Convert a dictionary to a MidjourneyPrompt.

    Args:
        prompt_dict: Dictionary containing prompt data.

    Returns:
        MidjourneyPrompt instance.
    """
    parser = MidjourneyParser()
    return parser.parse_dict(prompt_dict)
