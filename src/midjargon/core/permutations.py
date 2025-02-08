#!/usr/bin/env python3
# this_file: src/midjargon/core/permutations.py



def find_unescaped(s: str, char: str, start: int = 0) -> int:
    """Find the next unescaped occurrence of a character.

    Args:
        s: String to search in.
        char: Character to find.
        start: Starting position for search.

    Returns:
        Index of the first unescaped occurrence, or -1 if not found.
    """
    i = start
    while i < len(s):
        if s[i] == "\\":
            i += 2  # Skip escaped character
            continue
        if s[i] == char:
            return i
        i += 1
    return -1


def split_unescaped(s: str, delimiter: str = ",") -> list[str]:
    """Split string on unescaped delimiters and handle escapes.

    Args:
        s: String to split.
        delimiter: Character to split on.

    Returns:
        List of substrings.
    """
    parts = []
    current = []
    i = 0

    while i < len(s):
        if s[i] == "\\":
            if i + 1 < len(s):
                current.append(s[i + 1])  # Keep escaped character
                i += 2
            else:
                current.append(s[i])  # Keep trailing backslash
                i += 1
        elif s[i] == delimiter:
            parts.append("".join(current).strip())
            current = []
            i += 1
        else:
            current.append(s[i])
            i += 1

    if current:
        parts.append("".join(current).strip())

    return parts


def find_matching_brace(s: str, start: int) -> tuple[int, str]:
    """Find matching closing brace and extract error message if any.

    Args:
        s: String to search in.
        start: Position of opening brace.

    Returns:
        Tuple of (position of closing brace, error message).
        Position will be -1 if no match found.
    """
    count = 1
    i = start + 1

    while i < len(s):
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == "{":
            count += 1
        elif s[i] == "}":
            count -= 1
            if count == 0:
                return i, ""
        i += 1

    if count > 0:
        return -1, f"Unclosed brace at position {start}"
    return -1, "Invalid brace structure"


def expand_permutations(s: str) -> list[str]:
    """Recursively expand permutations in the prompt string using {a, b, ...} syntax.

    Handles:
    - Nested permutation groups
    - Escaped characters (\\, \\{, \\}, \\,)
    - Proper error reporting

    Args:
        s: String containing permutation groups.

    Returns:
        List of all possible permutations.

    Raises:
        ValueError: If the permutation syntax is invalid.
    """
    # Find first unescaped opening brace
    start = find_unescaped(s, "{")
    if start == -1:
        return [s]

    # Find matching closing brace
    end, error = find_matching_brace(s, start)
    if end == -1:
        raise ValueError(error)

    # Extract and split options
    options_str = s[start + 1 : end]
    try:
        options = split_unescaped(options_str)
    except Exception as e:
        msg = f"Failed to parse options at position {start}: {e!s}"
        raise ValueError(msg)

    if not options:
        msg = f"Empty permutation group at position {start}"
        raise ValueError(msg)

    # Recursively expand each option
    results = []
    prefix = s[:start]
    suffix = s[end + 1 :]

    for option in options:
        # Replace the entire '{...}' with the option
        new_s = prefix + option + suffix
        try:
            results.extend(expand_permutations(new_s))
        except Exception as e:
            msg = f"Failed to expand option '{option}': {e!s}"
            raise ValueError(msg)

    return results
