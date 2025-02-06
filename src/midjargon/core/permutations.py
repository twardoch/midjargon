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
            # Keep escaped characters as-is
            if text[i + 1] in (",", "{", "}"):
                current.append(text[i + 1])
            else:
                current.extend([text[i], text[i + 1]])
            i += ESCAPE_SEQUENCE_LENGTH
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
            if opt or not options:  # Include empty options
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
        start: Starting position of opening brace.

    Returns:
        Position of matching closing brace.

    Raises:
        ValueError: If no matching brace is found.
    """
    depth = 0
    pos = start
    while pos < len(text):
        if pos > 0 and text[pos - 1] == "\\":
            pos += 1
            continue
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return pos
        pos += 1
    msg = "No matching closing brace found"
    raise ValueError(msg)


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
    # Handle empty option
    if not option:
        return before.rstrip() + "  " + after.lstrip()  # Double space for empty option

    # Handle parameters
    if "--" in after:
        return f"{before.rstrip()} {option} {after.lstrip()}"

    # Handle spacing around the option
    result = before.rstrip()
    if result:
        result += " "
    result += option
    if after:
        result += " " + after.lstrip()
    return result.strip()


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


def split_permutation_options(text: str) -> list[str]:
    """
    Split permutation text into individual options.

    Args:
        text: Text to split.

    Returns:
        List of options.
    """
    if not text:
        return [""]

    options = []
    current = []
    in_quotes = False
    pos = 0

    while pos < len(text):
        char = text[pos]
        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
        elif char == "," and not in_quotes:
            options.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        pos += 1

    if current:
        options.append("".join(current).strip())

    return options


def expand_permutations(text: str) -> list[str]:
    """
    Expand all permutations in a text string.

    Args:
        text: Text to expand.

    Returns:
        List of expanded texts.

    Raises:
        ValueError: If permutation syntax is invalid.
    """
    if not text:
        return [""]

    result = [""]
    pos = 0

    while pos < len(text):
        if pos > 0 and text[pos - 1] == "\\":
            # Handle escaped characters
            for i in range(len(result)):
                result[i] += text[pos]
            pos += 1
            continue

        if text[pos] == "{":
            try:
                end = _find_matching_brace(text, pos)
                prefix = result[:]
                result = []
                options = split_permutation_options(text[pos + 1 : end])
                
                for p in prefix:
                    for opt in options:
                        result.append(p + opt)
                
                pos = end + 1
            except ValueError as e:
                msg = f"Invalid permutation syntax: {str(e)}"
                raise ValueError(msg) from e
        else:
            for i in range(len(result)):
                result[i] += text[pos]
            pos += 1

    return result
