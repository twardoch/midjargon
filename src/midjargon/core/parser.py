#!/usr/bin/env python3
# this_file: src/midjargon/core/parser.py

from typing import Any
from urllib.parse import urlparse

from pydantic import HttpUrl

from midjargon.core.models import CharacterReference, MidjourneyPrompt, StyleReference


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


def is_url(text: str) -> bool:
    """Check if text is a URL."""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def extract_image_urls(prompt: str) -> tuple[list[HttpUrl], str]:
    """Extract image URLs from the start of a prompt.

    Args:
        prompt: The raw prompt string.

    Returns:
        A tuple of (list of image URLs, remaining text).
    """
    parts = prompt.strip().split()
    urls = []
    text_start = 0

    for i, part in enumerate(parts):
        if is_url(part):
            urls.append(HttpUrl(part))
            text_start = i + 1
        else:
            break

    return urls, " ".join(parts[text_start:])


def parse_parameters(param_str: str) -> dict[str, Any]:
    """Parse parameter string into a dictionary.

    Args:
        param_str: The parameter string to parse.

    Returns:
        Dictionary of parameter names and values.

    Raises:
        ValueError: If parameter parsing fails.
    """
    params: dict[str, Any] = {
        "character_reference": [],
        "style_reference": [],
    }

    # Split into individual parameters
    parts = param_str.split("--")
    for part in parts[1:]:  # Skip empty first part
        if not part.strip():
            continue

        # Split parameter name and value
        param_parts = part.strip().split(maxsplit=1)
        param_name = param_parts[0]
        param_value = param_parts[1] if len(param_parts) > 1 else None

        # Handle special parameters
        if param_name == "cref":
            if param_value:
                if is_url(param_value):
                    params["character_reference"].append(
                        CharacterReference(url=HttpUrl(param_value), code=None)
                    )
                else:
                    params["character_reference"].append(
                        CharacterReference(url=None, code=param_value)
                    )
        elif param_name == "sref":
            if param_value:
                if is_url(param_value):
                    params["style_reference"].append(
                        StyleReference(url=HttpUrl(param_value), code=None)
                    )
                else:
                    params["style_reference"].append(
                        StyleReference(url=None, code=param_value)
                    )
        # Handle flag parameters
        elif param_value is None:
            params[param_name] = True
        # Handle numeric parameters
        elif param_value.replace(".", "").isdigit():
            if "." in param_value:
                params[param_name] = float(param_value)
            else:
                params[param_name] = int(param_value)
        # Handle boolean parameters
        elif param_value.lower() in ("true", "false"):
            params[param_name] = param_value.lower() == "true"
        # Handle list parameters
        elif param_value.startswith("[") and param_value.endswith("]"):
            try:
                items = [
                    item.strip()
                    for item in param_value[1:-1].split(",")
                    if item.strip()
                ]
                params[param_name] = items
            except Exception as e:
                msg = f"Failed to parse list parameter {param_name}: {e!s}"
                raise ValueError(msg)
        # Handle string parameters
        else:
            params[param_name] = param_value

    return params


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
        parameters = {
            "character_reference": [],
            "style_reference": [],
        }

    # Create and validate the prompt object
    try:
        return MidjourneyPrompt(
            text=text_part,
            image_prompts=images,
            **parameters,
        )
    except Exception as e:
        msg = f"Failed to create prompt object: {e!s}"
        raise ValueError(msg)


def parse_midjargon_prompt_to_dict(prompt: str) -> dict[str, Any]:
    """Parse a Midjourney prompt into a dictionary.

    Args:
        prompt: The raw prompt string to parse.

    Returns:
        Dictionary representation of the prompt.
    """
    parsed = parse_midjargon_prompt(prompt)
    return parsed.model_dump()
