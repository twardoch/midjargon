#!/usr/bin/env python3
# this_file: src/midjargon/core/input.py
from __future__ import annotations

from midjargon.core.models import PromptVariant
from midjargon.core.parser import parse_midjargon_prompt
from midjargon.core.permutations import expand_permutations

from midjargon.core.permutations import expand_text
# reuse the existing expansion logic
from midjargon.core.type_defs import MidjargonInput, MidjargonList


def expand_midjargon_input(prompt: MidjargonInput) -> MidjargonList:
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

    # Normalize weights to sum to 1.0
    total_weight = sum(weight for _, weight in result)
    if total_weight > 0:
        result = [(text, weight / total_weight) for text, weight in result]

    return result


def expand_midjargon_input(prompt: str) -> list[PromptVariant]:
    """Expand a midjourney prompt by processing permutations and returning a list of prompt variants.

    Args:
        prompt: A raw MidjargonInput string that may contain permutation syntax (e.g. {red, blue}).

    Returns:
        A list of PromptVariant objects, each containing an expanded prompt.

    Raises:
        ValueError: If the prompt is invalid or empty.
    """
    # First split into weighted prompts
    weighted_prompts = parse_weighted_prompt(prompt)

    # Process each weighted prompt
    result = []
    for text, weight in weighted_prompts:
        # Expand permutations for this prompt
        expanded = expand_permutations(text)
        for expanded_text in expanded:
            # Parse the expanded text into a MidjourneyPrompt
            try:
                prompt_obj = parse_midjargon_prompt(expanded_text)
                variant = PromptVariant(prompt=prompt_obj, weight=weight)
                # Ensure the weight is properly set in both places
                variant.prompt.weight = weight
                result.append(variant)
            except ValueError as e:
                msg = f"Failed to parse expanded prompt '{expanded_text}': {e}"
                raise ValueError(msg) from e

    return result
