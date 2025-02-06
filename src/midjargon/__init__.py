"""
midjargon

A Python library for parsing and manipulating Midjourney prompts.
"""

from importlib import metadata

from .midjargon import MidjargonPrompt, parse_prompt
from .midjourney import MidjourneyPrompt, parse_midjourney

__version__ = metadata.version(__name__)
__all__ = [
    "MidjargonPrompt",
    "MidjourneyPrompt",
    "parse_midjourney",
    "parse_prompt",
]
