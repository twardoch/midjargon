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
    """Handle errors with rich formatting."""
    if isinstance(error, ValueError | TypeError):
        # Handle expected errors nicely
        console.print(f"[red]Error:[/red] {error!s}")
    else:
        # For unexpected errors, show the full traceback
        console.print_exception()
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as JSON to stdout."""


def main(
    prompt: str,
    *,  # Make all following arguments keyword-only
    raw: bool = False,
    json_output: bool = False,
    no_color: bool = False,
) -> None:
    """
    Parse and validate a Midjourney prompt.

    Args:
        prompt: The Midjourney prompt string to parse.
        raw: If True, show the raw parsed structure before validation.
        json_output: If True, output in JSON format.
        no_color: If True, disable colored output.

    Example prompts:
        "A portrait of a wise old man --style raw --v 5.1"
        "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
        "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
        "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
        "elephant {, --s {200, 300}}"
    """
    console = Console(force_terminal=not no_color)

    try:
        # First parse with midjargon
        if raw:
            # Parse and expand the input
            expanded = expand_midjargon_input(prompt)
            # Convert each expanded prompt to a dictionary
            midjargon_dicts = [parse_midjargon_prompt_to_dict(p) for p in expanded]

            if json_output:
                # Output raw parsed prompts as JSON
                _output_json(midjargon_dicts)
            else:
                for i, p in enumerate(midjargon_dicts, 1):
                    console.print(
                        Panel(
                            Syntax(
                                json.dumps(p, indent=2),
                                "json",
                                theme="monokai",
                            ),
                            title=f"[bold]Raw Prompt {i}[/bold]",
                        )
                    )
            return

        # Parse and validate with Midjourney rules
        # First expand the input
        expanded = expand_midjargon_input(prompt)
        # Convert each expanded prompt to a dictionary
        midjargon_dicts = [parse_midjargon_prompt_to_dict(p) for p in expanded]
        # Parse each dictionary into a MidjourneyPrompt
        prompts = [parse_midjourney_dict(d) for d in midjargon_dicts]

        if json_output:
            # Output validated prompts as JSON
            _output_json([p.model_dump() for p in prompts])
        else:
            for i, p in enumerate(prompts, 1):
                if len(prompts) > 1:
                    console.print(f"\n[bold]Prompt {i}:[/bold]")

                # Show formatted prompt
                formatted = format_prompt(p)
                console.print(
                    Panel(
                        formatted,
                        title="[bold]Formatted[/bold]",
                        style="green",
                    )
                )

                # Show structured data
                console.print(
                    Panel(
                        Syntax(
                            p.model_dump_json(indent=2),
                            "json",
                            theme="monokai",
                        ),
                        title="[bold]Structured[/bold]",
                    )
                )

    except Exception as e:
        _handle_error(console, e)


if __name__ == "__main__":
    fire.Fire(main)
