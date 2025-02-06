#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

"""
permutations.py

Handles expansion of permutation expressions in Midjourney prompts.
Supports nested permutations and proper spacing handling.
"""

from collections.abc import Sequence

from .type_defs import MidjargonList

# Constants
ESCAPE_SEQUENCE_LENGTH = 2  # Length of escape sequence: backslash + character


def split_options(text: str) -> list[str]:
    """
    Split permutation options handling escaped commas and nested braces.

    Args:
        text: Text inside {} brackets containing comma-separated options.

    Returns:
        List of individual options with escaped characters unescaped.
    """
    options = []
    current = []
    i = 0
    depth = 0  # Track nested braces

    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            if text[i + 1] in (",", "{", "}"):
                current.append(text[i + 1])
                i += ESCAPE_SEQUENCE_LENGTH
            else:
                current.append(text[i])
                i += 1
        elif text[i] == "{":
            depth += 1
            current.append(text[i])
            i += 1
        elif text[i] == "}":
            depth -= 1
            current.append(text[i])
            i += 1
        elif text[i] == "," and depth == 0:
            # Add current option after stripping whitespace
            opt = "".join(current).strip()
            options.append(opt)
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1

    # Add the last option after stripping whitespace
    if current or not options:
        opt = "".join(current).strip()
        options.append(opt)

    return options


def _find_matching_brace(text: str, start: int) -> int:
    """
    Find the matching closing brace for an opening brace.

    Args:
        text: Text to search in.
        start: Index of opening brace.

    Returns:
        Index of matching closing brace or -1 if not found.
    """
    count = 1
    i = start + 1
    while i < len(text):
        if text[i] == "{":
            count += 1
        elif text[i] == "}":
            count -= 1
            if count == 0:
                return i
        i += 1
    return -1


def _format_part(before: str, option: str, after: str) -> str:
    """
    Format a permutation part with proper spacing.

    Args:
        before: Text before the permutation.
        option: The current option being formatted.
        after: Text after the permutation.

    Returns:
        Formatted text with proper spacing.
    """
    if option.startswith("--"):
        # For parameter permutations, preserve exact spacing
        return f"{before}{option}{after}".strip()
    # Combine parts and collapse multiple spaces
    return " ".join((before + option + after).split())


def _add_spacing(before: str, after: str) -> tuple[str, str]:
    """
    Add spacing between words if needed.

    Args:
        before: Text before permutation.
        after: Text after permutation.

    Returns:
        Tuple of (before, after) with proper spacing added.
    """
    if before and before[-1].isalnum():
        before = before + " "
    if after and after[0].isalnum():
        after = " " + after
    return before, after


def _expand_nested(options: Sequence[str]) -> MidjargonList:
    """
    Recursively expand any nested permutations in options.

    Args:
        options: List of options that may contain nested permutations.

    Returns:
        List of fully expanded options.
    """
    expanded = []
    for opt in options:
        if "{" in opt:
            expanded.extend(expand_single(opt))
        else:
            expanded.append(opt)
    return expanded


def expand_single(text: str) -> MidjargonList:
    """
    Expand a single level of permutation in text.

    Args:
        text: Text containing permutations in {} brackets.

    Returns:
        List of expanded variations.
    """
    results = []
    i = 0

    while i < len(text):
        if text[i] == "{":
            end = _find_matching_brace(text, i)
            if end == -1:
                return [text]  # Unmatched brace - treat as literal

            before = text[:i].rstrip()
            options = split_options(text[i + 1 : end])
            after = text[end + 1 :].lstrip()

            before, after = _add_spacing(before, after)

            # Recursively expand nested permutations
            expanded = _expand_nested(options)

            # Combine with surrounding text
            results = [_format_part(before, opt, after) for opt in expanded]
            break
        i += 1

    # No permutations found
    if not results:
        results = [text]

    return [r.strip() for r in results]


def expand_text(text: str) -> MidjargonList:
    """
    Expand all permutations in text into separate complete prompts.

    Args:
        text: Text containing permutations in {} brackets.

    Returns:
        List of expanded variations with all permutations resolved.
    """
    expanded = [text] if text else [""]
    max_iterations = 100  # Safety limit to prevent infinite loops
    iterations = 0

    while any("{" in t for t in expanded):
        next_level = []
        for t in expanded:
            next_level.extend(expand_single(t))

        # If no changes were made or we hit the iteration limit, break
        if set(next_level) == set(expanded) or iterations >= max_iterations:
            break

        expanded = next_level
        iterations += 1

    return expanded
