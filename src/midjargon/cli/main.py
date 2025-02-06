#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///

"""
midjargon.cli.main
~~~~~~~~~~~~~~~~~

A CLI tool that parses and validates Midjourney prompts.
Supports both raw parsing and Midjourney-specific validation.
"""

import json
import sys
from typing import Any, NoReturn

import fire
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.traceback import install

from midjargon import expand_midjargon_input, parse_midjargon_prompt_to_dict
from midjargon.engines.midjourney import MidjourneyPrompt, parse_midjourney_dict

# Install rich traceback handler
install(show_locals=True)

# Constants
NIJI_PREFIX_LENGTH = 4  # Length of "niji" in version string


def _format_numeric_params(prompt: MidjourneyPrompt) -> list[str]:
    """Format numeric parameters into command strings."""
    params = []
    if prompt.stylize is not None:
        params.append(f"--stylize {prompt.stylize}")
    if prompt.chaos is not None:
        params.append(f"--chaos {prompt.chaos}")
    if prompt.weird is not None:
        params.append(f"--weird {prompt.weird}")
    if prompt.image_weight is not None:
        params.append(f"--iw {prompt.image_weight}")
    if prompt.seed is not None:
        params.append(f"--seed {prompt.seed}")
    if prompt.stop is not None:
        params.append(f"--stop {prompt.stop}")
    return params


def _format_style_params(prompt: MidjourneyPrompt) -> list[str]:
    """Format style-related parameters into command strings."""
    params = []
    if prompt.style:
        params.append(f"--style {prompt.style}")
    if prompt.version:
        if prompt.version.startswith("niji"):
            params.append(
                f"--niji{' ' + prompt.version[5:] if len(prompt.version) > NIJI_PREFIX_LENGTH else ''}"
            )
        else:
            params.append(f"--v {prompt.version[1:]}")
    if prompt.personalization is not None:
        params.append(
            f"--p{' ' + prompt.personalization if prompt.personalization else ''}"
        )
    return params


def _format_extra_params(extra_params: dict[str, str | None]) -> list[str]:
    """Format extra parameters into command strings."""
    params = []
    for name, value in extra_params.items():
        if value is not None:
            params.append(f"--{name} {value}")
        else:
            params.append(f"--{name}")
    return params


def format_prompt(prompt: MidjourneyPrompt) -> str:
    """Format a MidjourneyPrompt for display."""
    parts = []

    # Add image URLs
    parts.extend(prompt.image_prompts)

    # Add text
    parts.append(prompt.text)

    # Build parameters list
    params = []

    # Handle aspect ratio
    if prompt.aspect_width and prompt.aspect_height:
        params.append(f"--ar {prompt.aspect_width}:{prompt.aspect_height}")

    # Add all parameter types
    params.extend(_format_numeric_params(prompt))
    params.extend(_format_style_params(prompt))
    params.extend(_format_extra_params(prompt.extra_params))

    if params:
        parts.append(" ".join(params))

    return " ".join(parts)


def _handle_error(console: Console, error: Exception) -> NoReturn:
    """Handle errors by printing to stderr and exiting."""
    error_console = Console(stderr=True)
    error_console.print(f"Error: {str(error)}", style="red")
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as JSON."""
    print(json.dumps(data, indent=2))


def process_prompt(prompt: str) -> list[MidjourneyPrompt]:
    """
    Process a prompt string into a list of MidjourneyPrompt objects.

    Args:
        prompt: The prompt text to process.

    Returns:
        List of MidjourneyPrompt objects.

    Raises:
        ValueError: If the prompt is invalid.
    """
    # Expand any permutations in the prompt
    expanded_prompts = expand_midjargon_input(prompt)

    # Process each expanded prompt
    results = []
    for expanded in expanded_prompts:
        # Parse into dictionary
        prompt_dict = parse_midjargon_prompt_to_dict(expanded)
        # Convert to MidjourneyPrompt
        prompt_obj = parse_midjourney_dict(prompt_dict)
        results.append(prompt_obj)

    return results


def main(
    prompt: str,
    raw: bool = False,
    json_output: bool = False,
    no_color: bool = False,
) -> None:
    """
    Main entry point for the CLI.

    Args:
        prompt: Input prompt to process.
        raw: Whether to output raw text only.
        json_output: Whether to output JSON.
        no_color: Whether to disable color output.
    """
    try:
        if not prompt.strip():
            msg = "Empty prompt"
            raise ValueError(msg)

        # Process the prompt
        results = process_prompt(prompt)

        if json_output:
            # Convert results to JSON-serializable format and output
            output = [result.model_dump() for result in results]
            print(json.dumps(output, indent=2))
            return

        # Format output
        console = Console(force_terminal=not no_color)
        if raw:
            for result in results:
                console.print(result.text)
        else:
            # Show formatted output
            panel = Panel(
                "\n".join(result.text for result in results),
                title="Formatted",
                expand=False,
            )
            console.print(panel)

            # Show structured output
            if len(results) == 1:
                panel = Panel(
                    json.dumps(results[0].model_dump(), indent=2),
                    title="Structured",
                    expand=False,
                )
                console.print(panel)
    except Exception as e:
        _handle_error(Console(stderr=True), e)


if __name__ == "__main__":
    fire.Fire(main)
