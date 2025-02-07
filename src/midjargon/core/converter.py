"""
TODO: Here are several end-user functionalites that our code can do. Your task is to implement the body of these functions, following the `TODO` indicators:

1. permute_prompt
2. parse_prompt
3. _prep_conversion
4. to_midjourney_prompts
5. to_fal_dicts

Let's modify the `cli` section of our code and expose these functions as Fire CLI commands. Move the existing CLI handling into a Fire `midjargon` command.
"""

from typing import Annotated as Doc

from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt_to_dict
from midjargon.core.type_defs import MidjargonDict
from midjargon.engines.fal import FalDict, to_fal_dict
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict


def permute_prompt(
    text: Doc[str, "Input prompt that may include permutation markers"],
) -> Doc[list[str], "List of permutated prompt strings"]:
    """
    Permute the input prompt, expanding it into a list of strings, by replacing permutation markers with actual values.

    Also, in our CLI, expose this as `permute` command.

    Args:
        text: The input prompt containing permutation markers.

    Returns:
        Always list of permutated prompt strings.
    """
    return expand_midjargon_input(text)


def parse_prompt(
    text: Doc[str, "Input prompt string"],
    permute: Doc[
        bool,
        "if true, we pass the prompt to permute_prompt first and then parse all prompts",
    ],
) -> Doc[MidjargonDict | list[MidjargonDict], "List of parsed prompt dicts"]:
    """
    Parse the input prompt into:
    - a single dict (if permute is False)
    - or either a single dict or a list of dicts (if permute is True). What we do is we permute and then we check the number of results. If there is only one result, we return a single dict. If there are multiple results, we return a list of dicts.

    Also, in our CLI, expose this as `json` command. In CLI.

    Args:
        text: The input prompt that may contain permutation markers if permute is True.
        permute: If True, we pass the prompt to permute_prompt first and then parse all prompts.

    Returns:
        A single dict or a list of dicts.
    """
    if not permute:
        return parse_midjargon_prompt_to_dict(text)

    expanded = permute_prompt(text)
    if not expanded:
        return parse_midjargon_prompt_to_dict(text)

    results = [parse_midjargon_prompt_to_dict(prompt) for prompt in expanded]
    return results[0] if len(results) == 1 else results


def _prep_conversion(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert, in various forms",
    ],
) -> Doc[list[MidjargonDict], "List of MidJargonDicts"]:
    """
    If input is:
        - a single str, permute it and call this function on the list of the result strings
        - a list of strings, call parse_prompt on each, then call this function again on the resulting list of dicts
        - a single dict, treat it as a single-item list of dicts
    Return:
        - a list of MidJargonDict
    """
    if isinstance(prompt, str):
        expanded = permute_prompt(prompt)
        return _prep_conversion(expanded)

    if isinstance(prompt, list):
        if not prompt:
            return []
        if all(isinstance(p, str) for p in prompt):
            dicts = [parse_prompt(str(p), permute=False) for p in prompt]
            if isinstance(dicts[0], list):
                return dicts[0]  # type: ignore
            return [dicts[0]]  # type: ignore
        if all(isinstance(p, dict) for p in prompt):
            return list(prompt)  # type: ignore
        msg = f"Unsupported list item type: {type(prompt[0])}"
        raise ValueError(msg)

    if isinstance(prompt, dict):
        return [prompt]

    msg = f"Unsupported prompt type: {type(prompt)}"
    raise ValueError(msg)


def to_midjourney_prompts(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert as Midjourney prompt",
    ],
) -> Doc[MidjourneyPrompt | list[MidjourneyPrompt], "Midjourney prompt(s)"]:
    """
    Convert the input prompt(s) into a Midjourney prompt(s). Pass the inputs to _prep_conversion and then take the resulting list of dicts and perform the actual conversion, calling parse_midjourney_dict on each, and prepare a list of MidjourneyPrompt results.

    Also, in our CLI, expose this as `midjourney` command.

    Return:
        - a single MidjourneyPrompt if we only have one result
        - a list of MidjourneyPrompt if we have multiple results
    """
    dicts = _prep_conversion(prompt)
    if not dicts:
        msg = "No valid prompts found"
        raise ValueError(msg)

    results = [parse_midjourney_dict(d) for d in dicts]
    return results[0] if len(results) == 1 else results


def to_fal_dicts(
    prompt: Doc[
        str | list[str] | MidjargonDict | list[MidjargonDict],
        "Prompt(s) to convert as Fal prompt",
    ],
) -> Doc[FalDict | list[FalDict], "Fal prompt(s)"]:
    """
    Convert the input prompt(s) into a Midjourney prompt(s). Pass the inputs to _prep_conversion and then take the resulting list of dicts and perform the actual conversion, calling to_fal_dict on each, and prepare a list of FalDict results.

    Also, in our CLI, expose this as `fal` command.

    Return:
        - a single FalDict if we only have one result
        - a list of FalDict if we have multiple results
    """
    dicts = _prep_conversion(prompt)
    if not dicts:
        msg = "No valid prompts found"
        raise ValueError(msg)

    results = [to_fal_dict(d) for d in dicts]
    return results[0] if len(results) == 1 else results
