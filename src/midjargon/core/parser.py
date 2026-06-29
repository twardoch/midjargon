#!/usr/bin/env python3
# this_file: src/midjargon/core/parser.py
"""
Parse a single (already-expanded) Midjourney prompt string into either a
flat ``MidjargonDict`` or a validated ``MidjourneyPrompt`` Pydantic model.

This module is intentionally permissive: unknown parameters are stored in
``extra_params``; no range validation is performed here (that is the engine's
responsibility).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from midjargon.core.parameters import parse_parameters
from midjargon.core.type_defs import MidjargonDict, MidjargonPrompt

if TYPE_CHECKING:
    from midjargon.core.models import MidjourneyPrompt as MJPrompt

# ---------------------------------------------------------------------------
# Numeric parameters that should be converted from string → int/float
# ---------------------------------------------------------------------------
_NUMERIC_PARAMS: frozenset[str] = frozenset(
    {
        "stylize",
        "chaos",
        "weird",
        "image_weight",
        "quality",
        "character_weight",
        "style_weight",
        "style_version",
        "repeat",
        "stop",
        # seed is intentionally excluded: converted by MidjourneyParameters validator
    }
)

_SEED_SPECIAL = frozenset({"random", "none"})


def _is_url(s: str) -> bool:
    return s.startswith(("http://", "https://"))


def _extract_images(prompt: str) -> tuple[list[str], str]:
    """Pull leading URL tokens out of *prompt*; return (urls, remainder)."""
    parts = prompt.split()
    urls: list[str] = []
    idx = 0
    for i, part in enumerate(parts):
        if _is_url(part):
            urls.append(part)
            idx = i + 1
        else:
            break
    return urls, " ".join(parts[idx:])


def _convert_numeric(value: str) -> int | float:
    f = float(value)
    return int(f) if f.is_integer() else f


def parse_midjargon_prompt_to_dict(prompt: str) -> MidjargonDict:
    """Parse an expanded prompt string into a flat dictionary.

    The returned dict always contains:
    - ``"text"``: normalised text portion (whitespace-collapsed)
    - ``"images"``: list of image URL strings (may be empty)
    - One key per parsed parameter (flag params → ``None``,
      multi-value params → ``list[str]``, others → str/int/float)

    No permutation expansion is performed; the caller is responsible for
    expanding ``{...}`` groups beforehand.

    Args:
        prompt: A single expanded prompt string.

    Returns:
        ``MidjargonDict`` with text, images, and parameter keys.
    """
    if not prompt or not prompt.strip():
        return {"text": "", "images": []}

    # 1. Extract leading image URLs
    images, remaining = _extract_images(prompt)

    # 2. Split text from parameters on the first " --"
    if " --" in remaining:
        text_raw, param_tail = remaining.split(" --", 1)
        param_str = "--" + param_tail
    else:
        text_raw = remaining
        param_str = ""

    # 3. Normalise text whitespace
    text = " ".join(text_raw.split())

    # 4. Parse raw parameters
    raw_params: dict[str, Any] = {}
    if param_str:
        try:
            raw_params = parse_parameters(param_str)
        except ValueError:
            # Tolerate unparseable param sections; store nothing
            raw_params = {}

    # 5. Build output dict, converting numeric strings
    result: MidjargonDict = {"text": text, "images": images}

    for key, value in raw_params.items():
        if (
            isinstance(value, str)
            and key in _NUMERIC_PARAMS
            and value not in _SEED_SPECIAL
        ):
            try:
                result[key] = _convert_numeric(value)
            except (ValueError, TypeError):
                result[key] = value
        else:
            result[key] = value

    return result


def parse_midjargon_prompt(prompt: str) -> MJPrompt:
    """Parse an expanded prompt string into a validated ``MidjourneyPrompt``.

    This is a convenience wrapper that calls
    :func:`parse_midjargon_prompt_to_dict` and then feeds the result through
    ``MidjourneyParser``.

    Args:
        prompt: A single expanded prompt string.

    Returns:
        A validated :class:`~midjargon.core.models.MidjourneyPrompt`.

    Raises:
        ValueError: If the prompt is empty or parameters are invalid.
    """
    from midjargon.engines.midjourney.midjourney import MidjourneyParser

    d = parse_midjargon_prompt_to_dict(prompt)
    # Rename "images" → "image_prompts" for the engine parser
    if "images" in d:
        d["image_prompts"] = d.pop("images")
    parser = MidjourneyParser()
    return parser.parse_dict(d)
