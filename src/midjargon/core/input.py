#!/usr/bin/env python3
# this_file: src/midjargon/core/input.py



from midjargon.core.models import PromptVariant
from midjargon.core.parser import parse_midjargon_prompt


def parse_weighted_prompt(prompt: str) -> list[tuple[str, float]]:
    """Parse a prompt with optional weights.

    Args:
        prompt: Raw prompt string with optional weights.

    Returns:
        List of (prompt, weight) tuples.

    Raises:
        ValueError: If prompt is empty or invalid.
    """
    if not prompt or not prompt.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    # Split on double colon and parse weights
    result = []
    current_prompt = []
    current_weight = None
    i = 0

    while i < len(prompt):
        if prompt[i : i + 2] == "::" and (i == 0 or prompt[i - 1] != "\\"):
            # Found weight separator
            text = "".join(current_prompt).strip()
            if not text:
                msg = "Empty prompt before weight"
                raise ValueError(msg)

            # Parse weight
            i += 2
            weight_start = i
            while i < len(prompt) and (prompt[i].isdigit() or prompt[i] == "."):
                i += 1

            if i == weight_start:
                msg = f"Missing weight after :: at position {i - 2}"
                raise ValueError(msg)

            try:
                weight = float(prompt[weight_start:i])
                if weight <= 0:
                    msg = f"Weight must be positive at position {weight_start}"
                    raise ValueError(msg)
            except ValueError as e:
                msg = f"Invalid weight at position {weight_start}: {prompt[weight_start:i]}"
                raise ValueError(msg) from e

            result.append((text, weight))
            current_prompt = []
            current_weight = None
        else:
            current_prompt.append(prompt[i])
            i += 1

    # Handle last part
    if current_prompt:
        text = "".join(current_prompt).strip()
        if text:
            result.append((text, 1.0))  # Default weight

    if not result:
        msg = "Empty prompt"
        raise ValueError(msg)

    return result


def expand_permutations(prompt: str) -> list[str]:
    """Expand permutations in a prompt.

    Args:
        prompt: Raw prompt string with permutations.

    Returns:
        List of expanded prompts.

    Raises:
        ValueError: If permutation syntax is invalid.
    """
    # Handle escaped braces and commas
    prompt = prompt.replace("\\{", "\x00").replace("\\}", "\x01").replace("\\,", "\x02")

    # Find all permutation groups
    groups = []
    start = 0
    depth = 0
    group_start = -1

    for i, char in enumerate(prompt):
        if char == "{":
            depth += 1
            if depth == 1:
                group_start = i
        elif char == "}":
            depth -= 1
            if depth == 0:
                groups.append((group_start, i))
            elif depth < 0:
                msg = "Unmatched closing brace"
                raise ValueError(msg)

    if depth > 0:
        msg = "Unclosed permutation group"
        raise ValueError(msg)

    # No permutations found
    if not groups:
        return [prompt.replace("\x00", "{").replace("\x01", "}").replace("\x02", ",")]

    # Process each group
    result = [""]
    pos = 0

    for start, end in groups:
        # Add text before group
        prefix = (
            prompt[pos:start]
            .replace("\x00", "{")
            .replace("\x01", "}")
            .replace("\x02", ",")
        )
        result = [r + prefix for r in result]

        # Get group options
        options = [
            o.strip()
            for o in prompt[start + 1 : end].split(",")
            if o.strip() or o.strip() == ""
        ]
        if not options:
            msg = "Empty permutation group"
            raise ValueError(msg)

        # Expand options
        new_result = []
        for r in result:
            for opt in options:
                new_result.append(
                    r
                    + opt.replace("\x00", "{").replace("\x01", "}").replace("\x02", ",")
                )
        result = new_result
        pos = end + 1

    # Add remaining text
    if pos < len(prompt):
        suffix = (
            prompt[pos:].replace("\x00", "{").replace("\x01", "}").replace("\x02", ",")
        )
        result = [r + suffix for r in result]

    return result


def expand_midjargon_input(prompt: str) -> list[PromptVariant]:
    """Expand a midjargon prompt by processing weights and permutations.

    Args:
        prompt: Raw prompt string with optional weights and permutations.

    Returns:
        List of PromptVariant objects.

    Raises:
        ValueError: If prompt parsing or expansion fails.
    """
    try:
        # Parse weighted prompts
        weighted_prompts = parse_weighted_prompt(prompt)
    except Exception as e:
        msg = f"Failed to parse weighted prompts: {e!s}"
        raise ValueError(msg)

    result = []

    for prompt_text, weight in weighted_prompts:
        try:
            # Expand permutations
            variants = expand_permutations(prompt_text)

            # Parse each variant
            for variant in variants:
                try:
                    parsed = parse_midjargon_prompt(variant)
                    result.append(PromptVariant(prompt=parsed, weight=weight))
                except Exception as e:
                    msg = f"Failed to parse variant '{variant}': {e!s}"
                    raise ValueError(msg)

        except Exception as e:
            msg = f"Failed to expand prompt '{prompt_text}': {e!s}"
            raise ValueError(msg)

    return result
