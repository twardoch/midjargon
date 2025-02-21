#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/midjourney.py

from typing import Any


from midjargon.core.models import (
    MidjourneyPrompt,
)


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
        text = prompt_dict.pop("text", "").strip()
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
