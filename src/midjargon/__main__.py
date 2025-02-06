#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///

"""
midimagine.py

A CLI tool that parses and validates Midjourney prompts.
Uses prompt_midjargon.py for initial parsing and prompt_midjourney.py for validation.
"""

import json

import fire
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from midjargon import parse_prompt
from prompt_midjourney import MidjourneyPrompt, parse_midjourney


def format_prompt(prompt: MidjourneyPrompt) -> str:
    """Format a MidjourneyPrompt for display."""
    parts = []

    # Add image URLs
    for img in prompt.image_prompts:
        parts.append(img.url)

    # Add text
    parts.append(prompt.text)

    # Add parameters
    params = []

    # Handle aspect ratio
    if prompt.aspect_width and prompt.aspect_height:
        params.append(f"--ar {prompt.aspect_width}:{prompt.aspect_height}")

    # Handle numeric parameters
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

    # Handle style parameters
    if prompt.style:
        params.append(f"--style {prompt.style}")
    if prompt.version:
        if prompt.version.startswith("niji"):
            params.append(
                f"--niji{' ' + prompt.version[5:] if len(prompt.version) > 4 else ''}"
            )
        else:
            params.append(f"--v {prompt.version[1:]}")

    # Add extra parameters
    for name, value in prompt.extra_params.items():
        if value is not None:
            params.append(f"--{name} {value}")
        else:
            params.append(f"--{name}")

    if params:
        parts.append(" ".join(params))

    return " ".join(parts)


def main(
    prompt: str,
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
            midjargon_prompts = parse_prompt(prompt)
            if json_output:
                pass
            else:
                for i, p in enumerate(midjargon_prompts, 1):
                    console.print(
                        Panel(
                            Syntax(
                                json.dumps(vars(p), indent=2),
                                "json",
                                theme="monokai",
                            ),
                            title=f"[bold]Raw Prompt {i}[/bold]",
                        )
                    )
            return

        # Parse and validate with Midjourney rules
        prompts = parse_midjourney(prompt)

        if json_output:
            pass
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
        console.print(f"[red]Error:[/red] {e!s}")
        raise SystemExit(1)


if __name__ == "__main__":
    fire.Fire(main)
