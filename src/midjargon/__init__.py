"""
midjargon

A Python library for parsing and manipulating Midjourney prompts.
"""

from importlib import metadata

from midjargon.core.input import expand_midjargon_input
from midjargon.core.models import (CharacterReference, ImageReference,
                                   MidjourneyParameters, MidjourneyPrompt,
                                   MidjourneyVersion, PromptVariant, StyleMode,
                                   StyleReference)
from midjargon.core.parser import (parse_midjargon_prompt,
                                   parse_midjargon_prompt_to_dict)

__all__ = [
    "MidjargonDict",
    # Core types
    "MidjargonInput",
    "MidjargonList",
    "MidjargonPrompt",
    # Midjourney-specific
    "MidjourneyPrompt",
    # Core functions
    "expand_midjargon_input",
    "parse_midjargon_prompt_to_dict",
    "parse_midjourney_dict",
]
