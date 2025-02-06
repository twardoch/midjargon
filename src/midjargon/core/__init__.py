"""
midjargon.core
~~~~~~~~~~~~~

Core functionality for prompt parsing and manipulation.

This module provides the base classes and utilities for:
- Prompt parsing and validation
- Parameter handling and normalization
- Text manipulation and splitting
- Type definitions for the midjargon package

The core module is engine-agnostic and provides the foundation for
specific engine implementations (like Midjourney).
"""

from .input import expand_midjargon_input
from .parameters import ParamDict, ParamName, ParamValue, parse_parameters
from .parser import parse_midjargon_prompt_to_dict
from .permutations import expand_text
from .type_defs import MidjargonDict, MidjargonInput, MidjargonList, MidjargonPrompt

__all__ = [
    "MidjargonDict",
    # Type definitions
    "MidjargonInput",
    "MidjargonList",
    "MidjargonPrompt",
    "ParamDict",
    "ParamName",
    "ParamValue",
    # Core functions
    "expand_midjargon_input",
    "expand_text",
    "parse_midjargon_prompt_to_dict",
    "parse_parameters",
]
