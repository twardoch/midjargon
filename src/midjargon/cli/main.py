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
                f"--niji{' ' + prompt.version[NIJI_PREFIX_LENGTH:] if len(prompt.version) > NIJI_PREFIX_LENGTH else ''}"
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
    error_console.print(f"Error: {error!s}", style="red")
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as formatted JSON without any Rich formatting."""
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.flush()


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
    *,  # Make all following arguments keyword-only
    raw: bool = False,
    json_output: bool = False,  # -j is an alias for --json_output
    no_color: bool = False,
) -> None:
    """
    Parse and validate a Midjourney prompt.

    Args:
        prompt: The Midjourney prompt string to parse.
        raw: If True, show the raw parsed structure before validation.
        json_output: If True, output in JSON format (alias: -j).
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
        # Expand permutations
        expanded = expand_midjargon_input(prompt)

        # Process each expanded prompt
        results = []
        for exp_prompt in expanded:
            # Parse into dictionary
            parsed = parse_midjargon_prompt_to_dict(exp_prompt)
            if raw:
                results.append(parsed)
                continue

            # Parse for Midjourney
            midjourney = parse_midjourney_dict(parsed)
            results.append(midjourney)

        if json_output:
            if raw:
                _output_json(results)
            else:
                # Convert Pydantic models to dicts for JSON serialization
                json_results = [prompt.model_dump() for prompt in results]
                _output_json(json_results)
            sys.stdout.flush()
            import time

            time.sleep(0.05)
            return

        # Display results
        for i, result in enumerate(results, 1):
            if len(results) > 1:
                console.print(f"\nVariant {i}:", style="bold blue")
            if raw:
                console.print(Panel(str(result)))
            else:
                console.print(Panel(format_prompt(result)))

    except Exception as error:
        if json_output:
            _output_json({"error": str(error)})
            sys.stdout.flush()
            sys.exit(1)
        else:
            _handle_error(console, error)


class MidjargonCLI:
    """Midjargon CLI interface."""

    def __call__(
        self,
        prompt: str,
        *,
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.

        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        return main(prompt, raw=raw, json_output=json_output, no_color=no_color)

    j = __call__  # Create alias for json_output as -j


if __name__ == "__main__":
    fire.Fire(MidjargonCLI())
