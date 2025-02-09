# this_file: src/midjargon/__init__.py
"""
midjargon

A Python library for parsing and manipulating Midjourney prompts.
"""

__version__ = "0.1.0"

from midjargon.core.input import expand_midjargon_input
from midjargon.core.models import MidjourneyPrompt, PromptVariant
from midjargon.core.parser import parse_midjargon_prompt_to_dict
from midjargon.engines.midjourney import MidjourneyParser, parse_midjourney_dict

__all__ = [
    "MidjourneyParser",
    "MidjourneyPrompt",
    "PromptVariant",
    "expand_midjargon_input",
    "parse_midjargon_prompt_to_dict",
    "parse_midjourney_dict",
]
