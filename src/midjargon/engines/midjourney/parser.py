#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/parser.py

from typing import Any

from midjargon.core.models import MidjourneyParameters, MidjourneyPrompt
from midjargon.core.parameters import parse_parameters


class MidjourneyParser:
    """Parser for Midjourney prompts."""

    def __init__(self, prompt_dict: dict[str, Any] | None = None):
        """Initialize the parser.

        Args:
            prompt_dict: Optional dictionary containing prompt data.
        """
        self.prompt_dict = prompt_dict or {}
        self.prompt = MidjourneyPrompt(
            text=self.prompt_dict.get("text", ""),
            images=self.prompt_dict.get("images", []),
            parameters=MidjourneyParameters(**self.prompt_dict.get("parameters", {})),
        )

    def parse(self) -> MidjourneyPrompt:
        """Parse the prompt data into a MidjourneyPrompt object.

        Returns:
            A validated MidjourneyPrompt object.
        """
        return self.prompt

    @staticmethod
    def from_string(prompt_str: str) -> "MidjourneyParser":
        """Create a parser from a prompt string.

        Args:
            prompt_str: The raw prompt string to parse.

        Returns:
            A MidjourneyParser instance.

        Raises:
            ValueError: If prompt parsing fails.
        """
        # Split into text and parameters
        if " --" in prompt_str:
            text_part, param_part = prompt_str.split(" --", 1)
            text_part = text_part.strip()
            param_str = "--" + param_part.strip()
            try:
                parameters = parse_parameters(param_str)
            except Exception as e:
                msg = f"Failed to parse parameters: {e!s}"
                raise ValueError(msg) from e
        else:
            text_part = prompt_str.strip()
            parameters = {}

        # Create prompt dictionary
        prompt_dict = {
            "text": text_part,
            "images": [],
            "parameters": parameters,
        }

        return MidjourneyParser(prompt_dict)
