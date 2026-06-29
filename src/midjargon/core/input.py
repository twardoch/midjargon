#!/usr/bin/env python3
# this_file: src/midjargon/core/input.py
"""
Expand permutation syntax in a raw Midjourney prompt string.

``expand_midjargon_input`` is the public entry point: it expands all
``{a, b}`` groups and unescapes ``\\{``, ``\\}``, ``\\,`` sequences,
returning a flat list of fully-resolved prompt strings.
"""

from __future__ import annotations

from midjargon.core.permutations import expand_permutations
from midjargon.core.type_defs import MidjargonInput, MidjargonList


def expand_midjargon_input(prompt: MidjargonInput) -> MidjargonList:
    """Expand permutation groups in *prompt* and return all variants.

    Args:
        prompt: Raw prompt string, possibly containing ``{opt1, opt2}``
                permutation groups and escape sequences.

    Returns:
        List of fully-expanded, unescaped prompt strings.  An empty input
        returns ``[""]``; a prompt without permutations returns a
        single-element list.
    """
    return expand_permutations(prompt)
