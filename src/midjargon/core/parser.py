#!/usr/bin/env python3
# this_file: src/midjargon/core/parser.py
from __future__ import annotations

Provides a simple, permissive parser that converts an expanded prompt (a MidjargonPrompt string)
into a flat dictionary (MidjargonDict) with the following keys:
  - "images": list of image URLs (extracted from the beginning of the prompt)
  - "text": the main text of the prompt
  - Additional keys for any parameters found (keys without the '--' prefix)

from midjargon.core.models import (CharacterReference, ImageReference,
                                   MidjourneyPrompt, MidjourneyVersion,
                                   StyleMode, StyleReference)
from pydantic import HttpUrl


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
    except Exception:
        return False


def is_url(text: str) -> bool:
    """Check if text is a URL."""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

    Args:
        text: The text to split.

def extract_image_urls(prompt: str) -> tuple[list[ImageReference], str]:
    """Extract image URLs from the start of a prompt.

    Args:
        tokens: List of tokens from prompt text.

    Returns:
        A tuple of (list of ImageReference objects, remaining text).
    """
    parts = prompt.strip().split()
    refs = []
    text_start = 0

    for i, part in enumerate(parts):
        if is_url(part):
            refs.append(ImageReference(url=HttpUrl(part)))
            text_start = i + 1
        else:
            break

    return refs, " ".join(parts[text_start:])


def parse_midjargon_prompt_to_dict(expanded_prompt: MidjargonPrompt) -> MidjargonDict:
    """
    Parse an expanded prompt into a dictionary format.
    Handles URL extraction and parameter parsing.

    Args:
        expanded_prompt: Expanded prompt string.

    Returns:
        Dictionary containing parsed prompt components.
    """
    # Extract URLs and text
    urls = []
    text_parts = []

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
        elif param_name == "ar":
            if param_value:
                try:
                    w, h = map(int, param_value.split(":"))
                    params["aspect_ratio"] = f"{w}:{h}"
                    params["aspect_width"] = w
                    params["aspect_height"] = h
                except ValueError as e:
                    msg = f"Invalid aspect ratio format: {e}"
                    raise ValueError(msg) from e
        elif param_name in ("v", "version"):
            if param_value:
                try:
                    version = MidjourneyVersion(param_value)
                    params["version"] = version
                except ValueError as e:
                    msg = f"Invalid version value: {param_value}"
                    raise ValueError(msg) from e
        elif param_name == "style":
            if param_value:
                try:
                    style = StyleMode(param_value.lower())
                    params["style"] = style
                except ValueError as e:
                    msg = f"Invalid style value: {param_value}"
                    raise ValueError(msg) from e
        # Handle flag parameters
        elif param_value is None:
            if param_name in {"tile", "turbo", "relax"}:
                params[param_name] = True
            else:
                msg = f"Invalid flag parameter: {param_name}"
                raise ValueError(msg)
        # Handle numeric parameters
        elif param_value.replace(".", "").isdigit():
            if param_name in {"stylize", "s"}:
                params["stylize"] = int(param_value)
            elif param_name in {"chaos", "c"}:
                params["chaos"] = int(param_value)
            elif param_name in {"weird", "w"}:
                params["weird"] = int(param_value)
            elif param_name == "seed" and param_value != "random":
                params["seed"] = int(param_value)
            elif param_name == "cw":
                params["character_weight"] = float(param_value)
            elif param_name == "sw":
                params["style_weight"] = float(param_value)
            else:
                params[param_name] = (
                    float(param_value) if "." in param_value else int(param_value)
                )
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
                raise ValueError(msg) from e
        # Handle string parameters
        else:
            text_parts.append(part)

    # Join remaining parts as text, preserving original spacing
    text_part = " ".join(text_parts)

    # Find where parameters start (if any)
    param_part = ""
    if "--" in text_part:
        text_split = text_part.split("--", 1)
        text_part = text_split[0].strip()
        param_part = "--" + text_split[1]

    # Parse parameters using the consolidated parameter parsing logic
    params = parse_parameters(param_part) if param_part.startswith("--") else {}

    # Convert numeric values
    numeric_params = {
        "stylize": int,
        "chaos": int,
        "weird": int,
        "image_weight": float,
        "seed": int,
        "stop": int,
        "quality": float,
        "repeat": int,
        "character_weight": int,
        "style_weight": int,
        "style_version": int,
    }

    for param, converter in numeric_params.items():
        if param in params and params[param] is not None:
            with contextlib.suppress(ValueError, TypeError):
                params[param] = converter(params[param])

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
            raise ValueError(msg) from e
    else:
        text_part = remaining_text.strip()
        parameters = {}

    # Create and validate the prompt object
    try:
        return MidjourneyPrompt(
            text=text_part,
            image_prompts=images,
            **parameters,
        )
    except Exception as e:
        msg = f"Failed to create prompt object: {e!s}"
        raise ValueError(msg) from e


def parse_midjargon_prompt_to_dict(prompt: str) -> dict[str, Any]:
    """Parse a Midjourney prompt into a dictionary.

    Args:
        prompt: The raw prompt string to parse.

    return cast(MidjargonDict, result)
