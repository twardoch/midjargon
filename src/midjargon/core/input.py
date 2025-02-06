"""
input.py

Contains functions for handling raw input.
Specifically, it expands all permutation expressions in a prompt without doing any parameter parsing/validation.
"""

from .permutations import expand_text  # reuse the existing expansion logic
from .type_defs import MidjargonInput, MidjargonList


def expand_midjargon_input(prompt: MidjargonInput) -> MidjargonList:
    """
    Expands a raw midjargon prompt string into a list of fully expanded prompt strings.

    Args:
        prompt: A raw MidjargonInput string that may contain permutation syntax (e.g. {red, blue}).

    Returns:
        A list of MidjargonPrompt strings with all permutation expressions resolved.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not prompt.strip():
        msg = "Empty prompt"
        raise ValueError(msg)

    # Handle escaped braces by temporarily replacing them
    processed = prompt.replace(r"\{", "‹").replace(r"\}", "›")
    expanded = expand_text(processed)
    # Restore escaped braces
    return [text.replace("‹", "{").replace("›", "}") for text in expanded]
