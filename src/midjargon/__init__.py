#!/usr/bin/env python3
# this_file: src/midjargon/__init__.py

"""Midjargon package for parsing and manipulating Midjourney-style prompts."""

__version__ = "0.1.0"

from midjargon.core.input import expand_midjargon_input
from midjargon.core.models import (
    CharacterReference,
    ImageReference,
    MidjourneyParameters,
    MidjourneyPrompt,
    MidjourneyVersion,
    PromptVariant,
    StyleMode,
    StyleReference,
)
from midjargon.core.parser import (
    parse_midjargon_prompt,
    parse_midjargon_prompt_to_dict,
)

__all__ = [
    "CharacterReference",
    "ImageReference",
    "MidjourneyParameters",
    "MidjourneyPrompt",
    "MidjourneyVersion",
    "PromptVariant",
    "StyleMode",
    "StyleReference",
    "expand_midjargon_input",
    "parse_midjargon_prompt",
    "parse_midjargon_prompt_to_dict",
]
