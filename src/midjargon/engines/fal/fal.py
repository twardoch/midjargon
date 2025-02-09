#!/usr/bin/env python3
# this_file: src/midjargon/engines/fal/fal.py

from typing import Any

from pydantic import BaseModel, HttpUrl, computed_field


class FalPrompt(BaseModel):
    """Fal.ai prompt model with all parameters."""

    text: str
    image_prompts: list[HttpUrl] = []
    negative_prompt: str | None = None
    num_inference_steps: int | None = 50
    guidance_scale: float | None = 7.5
    width: int | None = 1024
    height: int | None = 1024
    seed: int | None = None
    scheduler: str | None = None
    extra_params: dict[str, Any] = {}

    @computed_field
    @property
    def images(self) -> list[HttpUrl]:
        """Get image URLs."""
        return self.image_prompts

    @computed_field
    @property
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


class FalParser:
    """Parser for converting between Fal.ai prompt formats."""

    def parse_dict(self, prompt_dict: dict[str, Any]) -> FalPrompt:
        """Parse a dictionary into a FalPrompt.

        Args:
            prompt_dict: Dictionary containing prompt data.

        Returns:
            FalPrompt instance.

        Raises:
            ValueError: If the prompt text is empty.
        """
        # Validate text
        text = prompt_dict.get("text", "").strip()
        if not text:
            msg = "Empty prompt"
            raise ValueError(msg)

        # Extract known fields
        known_fields = set(FalPrompt.model_fields)

        # Split into known and extra parameters
        params = {}
        extra_params = {}
        for key, value in prompt_dict.items():
            if key in known_fields:
                params[key] = value
            else:
                extra_params[key] = value

        # Create prompt with all parameters
        return FalPrompt(text=text, **params, extra_params=extra_params)


def parse_fal_dict(prompt_dict: dict[str, Any]) -> FalPrompt:
    """Convert a dictionary to a FalPrompt.

    Args:
        prompt_dict: Dictionary containing prompt data.

    Returns:
        FalPrompt instance.
    """
    parser = FalParser()
    return parser.parse_dict(prompt_dict)
