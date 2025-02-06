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
    depth = 1  # Start at 1 since we're starting at an opening brace
    pos = start + 1
    while pos < len(text):
        # Check for escaped braces
        if text[pos - 1] == "\\" and text[pos] in {"{", "}"}:
            pos += 1
            continue
        if text[pos] == "{" and (pos == 0 or text[pos - 1] != "\\"):
            depth += 1
        elif text[pos] == "}" and (pos == 0 or text[pos - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return pos
        pos += 1
    # If we reach here, treat unmatched braces as literal text
    return start


def _extract_options(text: str, start: int, end: int) -> list[str]:
    """
    Extract comma-separated options from text between braces.

    Args:
        text: Text to extract from.
        start: Start position (after opening brace).
        end: End position (before closing brace).

    Returns:
        List of options.
    """
    # Extract the text between braces
    options_text = text[start + 1 : end]

    # Split on commas and handle escaped braces
    options = []
    current = []
    i = 0
    depth = 0

    while i < len(options_text):
        if i > 0 and options_text[i - 1] == "\\" and options_text[i] in {"{", "}", ","}:
            current.append(options_text[i])
            i += 1
            continue

        if options_text[i] == "{":
            depth += 1
            current.append(options_text[i])
        elif options_text[i] == "}":
            depth -= 1
            current.append(options_text[i])
        elif options_text[i] == "," and depth == 0:
            opt = "".join(current).strip()
            if opt or not options:  # Include empty options if it's the first one
                # Handle word boundaries
                if " " in opt:
                    opt = " ".join(part.strip() for part in opt.split())
                options.append(opt)
            current = []
        else:
            current.append(options_text[i])
        i += 1

    # Handle the last option
    opt = "".join(current).strip()
    if opt or not options:  # Include empty options if no other options exist
        # Handle word boundaries
        if " " in opt:
            opt = " ".join(part.strip() for part in opt.split())
        options.append(opt)

    return options


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
        return before.rstrip() + after.lstrip()

    # Handle word boundaries
    result = before.rstrip()
    if result and not result.endswith(" "):
        result += " "
    result += option.strip()
    if after and not after.startswith(" "):
        result += " "
    result += after.lstrip()
    return result.rstrip()


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


def expand_single(text: str) -> list[str]:
    """
    Expand a single level of permutations in text.

    Args:
        text: Text to expand.

    Returns:
        List of expanded texts.
    """
    # Find first unescaped opening brace
    i = 0
    while i < len(text):
        if text[i] == "{" and (i == 0 or text[i - 1] != "\\"):
            break
        i += 1
    else:
        # No unescaped opening brace found
        return [text]

    # Find matching closing brace
    j = _find_matching_brace(text, i)
    if j == i:  # No matching brace found, treat as literal
        return [text]

    # Extract and process options
    options = _extract_options(text, i, j)
    if not options:  # Empty permutation
        return [_format_part(text[:i], "", text[j + 1 :])]

    # Generate permutations
    prefix = text[:i]
    suffix = text[j + 1 :]

    # Handle nested permutations
    expanded_options = []
    for opt in options:
        if opt == "":  # Handle empty option
            expanded_options.append("")
        elif "{" in opt:
            expanded = expand_text(opt)
            expanded_options.extend(expanded)
        else:
            expanded_options.append(opt)

    # Format each option with proper spacing
    results = []
    for opt in expanded_options:
        results.append(_format_part(prefix, opt, suffix))

    return results


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
    if not text.strip():
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

    # Filter out empty options
    options = [opt for opt in options if opt]
    if not options:
        return [""]

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
            except ValueError:
                # If no matching brace is found, treat as literal text
                for i in range(len(result)):
                    result[i] += text[pos]
                pos += 1
        else:
            for i in range(len(result)):
                result[i] += text[pos]
            pos += 1

    return result
