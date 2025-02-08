# this_file: src/midjargon/__init__.py
"""
midjargon

A Python library for parsing and manipulating Midjourney prompts.
"""

__version__ = "0.1.0"

__all__ = []

from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt_to_dict
