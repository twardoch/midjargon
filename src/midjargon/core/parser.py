#!/usr/bin/env python3
# this_file: src/midjargon/core/parser.py

import re
from typing import Any
from urllib.parse import urlparse

from pydantic import HttpUrl

from midjargon.core.models import (
    ImageReference,
    MidjourneyParameters,
    MidjourneyPrompt,
)
from midjargon.core.parameters import parse_parameters


def is_valid_image_url(url: str) -> bool:
    """Check if a URL is a valid image URL."""
    try:
        result = urlparse(url)
        return bool(
            result.scheme
            and result.netloc
            and any(
                result.path.lower().endswith(ext)
                for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
            )
        )
    except:
        return False


def extract_image_urls(prompt: str) -> tuple[list[ImageReference], str]:
    """Extract image URLs from a prompt string.

    Args:
        prompt: Raw prompt string.

    Returns:
        Tuple of (list of ImageReference objects, remaining text).
    """
    if isinstance(prompt, str):
        matches = re.finditer(r"(https?://\S+)", prompt)
        images = []
        last_end = 0
        remaining_parts = []

        for match in matches:
            start, end = match.span()
            remaining_parts.append(prompt[last_end:start])
            url = match.group(1)
            images.append(ImageReference(url=HttpUrl(url)))
            last_end = end

        remaining_parts.append(prompt[last_end:])
        remaining_text = " ".join(
            part.strip() for part in remaining_parts if part.strip()
        )
        return images, remaining_text
    else:
        return getattr(prompt, "images", []), str(prompt)


def parse_midjargon_prompt_to_dict(prompt: str) -> dict[str, Any]:
    """Parse a Midjourney prompt into a dictionary.

    Args:
        prompt: The raw prompt string to parse.

    Returns:
        Dictionary representation of the prompt.
    """
    parsed = parse_midjargon_prompt(prompt)
    return parsed.model_dump()


def parse_midjargon_prompt(prompt: str) -> MidjourneyPrompt:
    """Parse a Midjourney prompt into a validated MidjourneyPrompt object.

    Args:
        prompt: The raw prompt string to parse.

    Returns:
        A validated MidjourneyPrompt object.

    Raises:
        ValueError: If the prompt is invalid or missing required components.
    """
    # Extract image URLs
    images, remaining_text = extract_image_urls(prompt)

    # Split into text and parameters
    if " --" in remaining_text:
        text_part, param_part = remaining_text.split(" --", 1)
        text_part = text_part.strip()
        param_str = "--" + param_part.strip()
        try:
            parameters = parse_parameters(param_str)
        except Exception as e:
            msg = f"Failed to parse parameters: {e!s}"
            raise ValueError(msg)
    else:
        text_part = remaining_text.strip()
        parameters = {}

    # Create and validate the prompt object
    try:
        return MidjourneyPrompt(
            text=text_part, images=images, parameters=MidjourneyParameters(**parameters)
        )
    except Exception as e:
        msg = f"Failed to create prompt object: {e!s}"
        raise ValueError(msg)
