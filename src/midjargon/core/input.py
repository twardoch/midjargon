#!/usr/bin/env python3
# this_file: src/midjargon/core/input.py

from midjargon.core.models import MidjourneyPrompt, PromptVariant
from midjargon.core.permutations import expand_permutations


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


def expand_midjargon_input(prompt: str) -> list[PromptVariant]:
    """Expand a midjourney prompt by processing permutations and returning a list of prompt variants.

    Args:
        prompt: The prompt string to expand.

    Returns:
        A list of PromptVariant objects, each containing an expanded prompt.
    """
    permutation_options = expand_permutations(prompt)
    return [
        PromptVariant(prompt=MidjourneyPrompt(text=opt), weight=1.0)
        for opt in permutation_options
    ]
