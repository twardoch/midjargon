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
    error_console = Console(file=sys.stderr)
    error_console.print(f"Error: {str(error)}")
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as formatted JSON."""
    json_str = json.dumps(data, indent=2)
    print(json_str)


def main(
    prompt: str,
    *,  # Make all following arguments keyword-only
    raw: bool = False,
    json_output: bool = False,
    no_color: bool = False,
) -> None:
    """
    Process and validate a Midjourney prompt.

    Args:
        prompt: The prompt text to process.
        raw: If True, skip Midjourney-specific validation.
        json_output: If True, output in JSON format.
        no_color: If True, disable colored output.
    """
    # Create console for output
    console = Console(force_terminal=not no_color)
    error_console = Console(file=sys.stderr)

    try:
        # Expand any permutations in the prompt
        expanded_prompts = expand_midjargon_input(prompt)

        # Process each expanded prompt
        results = []
        for expanded in expanded_prompts:
            # Parse into dictionary
            prompt_dict = parse_midjargon_prompt_to_dict(expanded)

            # Validate as Midjourney prompt if not raw
            if not raw:
                prompt_dict = parse_midjourney_dict(prompt_dict).model_dump()

            results.append(prompt_dict)

        # Output results
        if json_output:
            if len(results) == 1:
                _output_json(results[0])
            else:
                _output_json(results)
            return

        # Format each result
        for result in results:
            if raw:
                # Display raw dictionary
                console.print(
                    Panel(
                        Syntax(
                            json.dumps(result, indent=2),
                            "json",
                            background_color="default",
                        ),
                        title="Raw",
                    )
                )
            else:
                # Display formatted prompt
                prompt_obj = MidjourneyPrompt(**result)
                formatted = format_prompt(prompt_obj)
                console.print(
                    Panel(formatted, title="Formatted"),
                    Panel(
                        Syntax(
                            json.dumps(result, indent=2),
                            "json",
                            background_color="default",
                        ),
                        title="Structured",
                    ),
                )

    except Exception as e:
        if isinstance(e, ValueError):
            print(f"Error: {str(e)}", file=sys.stderr)
        else:
            error_console.print_exception(show_locals=True)
        sys.exit(1)


if __name__ == "__main__":
    fire.Fire(main)
