#!/usr/bin/env python3
# this_file: src/midjargon/cli/main.py

import sys
from typing import Any

import fire
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from midjargon.core.input import expand_midjargon_input

# Create consoles for stdout and stderr
console = Console()
error_console = Console(stderr=True)


def strip_ansi(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text to strip ANSI codes from

    Returns:
        Plain text without ANSI codes
    """
    return Text.from_ansi(text).plain


def format_prompt_variant(variant, index: int | None = None) -> Panel:
    """Format a prompt variant as a Rich panel."""
    prompt = variant.prompt

    # Create table for parameters
    param_table = Table(show_header=False, box=None)
    param_dict = prompt.parameters.model_dump(exclude_none=True)
    for key, value in param_dict.items():
        param_table.add_row(f"--{key}", str(value))

    # Format content
    content = [
        "[bold blue]Text:[/] " + prompt.text,
    ]

    if prompt.images:
        content.append("\n[bold blue]Images:[/]")
        for img in prompt.images:
            content.append(f"  {img.url}")

    if param_dict:
        content.append("\n[bold blue]Parameters:[/]")
        content.append(param_table)

    if variant.weight != 1.0:
        content.append(f"\n[bold blue]Weight:[/] {variant.weight}")

    title = f"Variant {index}" if index is not None else None
    return Panel("\n".join(str(c) for c in content), title=title)


def format_json_output(
    variants: list[Any], include_parsed: bool = True
) -> dict[str, Any] | list[dict[str, Any]]:
    """Format variants for JSON output.

    Args:
        variants: List of prompt variants
        include_parsed: Whether to include parsed data

    Returns:
        Dictionary or list ready for JSON serialization
    """
    if len(variants) == 1:
        variant = variants[0]
        params = variant.prompt.parameters.model_dump(exclude_none=True)
        # Map parameter names to match test expectations
        param_mapping = {
            "aspect": "aspect_ratio",
            "stylize": "stylize",
            "chaos": "chaos",
            "weird": "weird",
            "quality": "quality",
            "personalization": "personalization",
            "version": "version",
            "tile": "tile",
            "turbo": "turbo",
            "relax": "relax",
            "no": "no",
            "style": "style",
            "seed": "seed",
            "character_reference": "character_reference",
            "style_reference": "style_reference",
            "character_weight": "character_weight",
            "style_weight": "style_weight",
            "style_version": "style_version",
        }
        mapped_params = {param_mapping.get(k, k): v for k, v in params.items()}
        result = {
            "text": variant.prompt.text,
            "images": [str(img.url) for img in variant.prompt.images],
            **mapped_params,
            "weight": variant.weight,
        }
        if include_parsed:
            result["parsed"] = variant.prompt.model_dump()
        return result
    else:
        return [
            {
                "text": v.prompt.text,
                "prompt": v.prompt.to_string(),
                "images": [str(img.url) for img in v.prompt.images],
                **v.prompt.parameters.model_dump(exclude_none=True),
                "weight": v.weight,
                **({"parsed": v.prompt.model_dump()} if include_parsed else {}),
            }
            for v in variants
        ]


class MidjargonCLI:
    """CLI interface for the midjargon package."""

    def mj(self, prompt: str, json_output: bool = False, no_color: bool = False):
        """Convert prompt to Midjourney format.

        Args:
            prompt: The prompt to convert.
            json_output: Whether to output in JSON format.
            no_color: Whether to disable colored output.
        """
        try:
            variants = expand_midjargon_input(prompt)

            if json_output:
                console.print_json(data=format_json_output(variants))
            else:
                with console.capture() as capture:
                    for i, variant in enumerate(variants, 1):
                        if i > 1:
                            console.print()
                        console.print(format_prompt_variant(variant, i))
                        console.print("\n[bold green]Midjourney Format:[/]")
                        console.print(variant.prompt.to_string())

                output = capture.get()
                if no_color:
                    console.print(strip_ansi(output))
                else:
                    console.print(output)

        except Exception as e:
            error_console.print(f"[bold red]Error:[/] {e!s}")
            return 1

    def json(self, prompt: str, json_output: bool = True, no_color: bool = False):
        """Parse prompt and output as JSON.

        Args:
            prompt: The prompt to parse.
            json_output: Whether to output in JSON format.
            no_color: Whether to disable colored output.
        """
        try:
            variants = expand_midjargon_input(prompt)

            if json_output:
                console.print_json(
                    data=format_json_output(variants, include_parsed=True)
                )
            else:
                with console.capture() as capture:
                    for i, variant in enumerate(variants, 1):
                        if i > 1:
                            console.print()
                        console.print(format_prompt_variant(variant, i))

                output = capture.get()
                if no_color:
                    console.print(strip_ansi(output))
                else:
                    console.print(output)

        except Exception as e:
            error_console.print(f"[bold red]Error:[/] {e!s}")
            return 1

    def perm(self, prompt: str, json_output: bool = False, no_color: bool = False):
        """Show all permutation variants.

        Args:
            prompt: The prompt to expand.
            json_output: Whether to output in JSON format.
            no_color: Whether to disable colored output.
        """
        try:
            variants = expand_midjargon_input(prompt)

            if json_output:
                console.print_json(
                    data=format_json_output(variants, include_parsed=False)
                )
            else:
                with console.capture() as capture:
                    for i, variant in enumerate(variants, 1):
                        if i > 1:
                            console.print()
                        console.print(format_prompt_variant(variant, i))

                output = capture.get()
                if no_color:
                    console.print(strip_ansi(output))
                else:
                    console.print(output)

        except Exception as e:
            error_console.print(f"[bold red]Error:[/] {e!s}")
            return 1

    def fal(self, prompt: str, json_output: bool = False, no_color: bool = False):
        """Convert prompt to Fal.ai format.

        Args:
            prompt: The prompt to convert.
            json_output: Whether to output in JSON format.
            no_color: Whether to disable colored output.
        """
        try:
            variants = expand_midjargon_input(prompt)

            if json_output:
                # TODO: Implement Fal.ai conversion
                console.print_json(data=format_json_output(variants))
            else:
                with console.capture() as capture:
                    for i, variant in enumerate(variants, 1):
                        if i > 1:
                            console.print()
                        console.print(format_prompt_variant(variant, i))
                        console.print("\n[bold green]Fal.ai Format:[/]")
                        # TODO: Implement Fal.ai conversion
                        console.print(variant.prompt.to_string())

                output = capture.get()
                if no_color:
                    console.print(strip_ansi(output))
                else:
                    console.print(output)

        except Exception as e:
            error_console.print(f"[bold red]Error:[/] {e!s}")
            return 1


def main():
    """Main entry point for the CLI."""
    try:
        fire.Fire(MidjargonCLI)
    except Exception as e:
        error_console.print(f"[bold red]Fatal Error:[/] {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
