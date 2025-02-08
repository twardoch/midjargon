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

import fire  # type: ignore
from rich.ansi import AnsiDecoder
from rich.console import Console, Group
from rich.panel import Panel
from rich.theme import Theme
from rich.traceback import install

from midjargon.core.converter import (
    parse_prompt,
    permute_prompt,
    to_fal_dicts,
    to_midjourney_prompts,
)
from midjargon.engines.midjourney.models import MidjourneyPrompt

install(show_locals=True)
ansi_decoder = AnsiDecoder()
console = Console(theme=Theme({"prompt": "cyan", "question": "bold cyan"}))


def display(lines, out):
    console.print(Group(*map(ansi_decoder.decode_line, lines)))


# Monkey patch fire's Display function
fire.Display = display  # type: ignore


def _handle_error(console: Console, error: Exception) -> NoReturn:
    """Handle errors by printing to stderr and exiting."""
    error_console = Console(stderr=True)
    error_console.print(f"Error: {error!s}", style="red")
    sys.exit(1)


def _output_json(data: Any) -> None:
    """Output data as formatted JSON without any Rich formatting."""
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.flush()


def _format_prompt(prompt: Any) -> str:
    """Format a prompt for display."""
    if hasattr(prompt, "model_dump"):
        return json.dumps(prompt.model_dump(), indent=2)
    return json.dumps(prompt, indent=2)


class MidjargonCLI:
    """Midjargon CLI interface."""

    def perm(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> list[str] | None:
        """
        Permute a prompt string, expanding all permutation markers.

        Args:
            prompt: The prompt string to permute.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A {red, blue, green} bird on a {branch, rock}"
            "elephant {, --s {200, 300}}"

        Returns:
            List of permuted prompts if successful, None if error occurs.
        """
        console = Console(force_terminal=not no_color)

        try:
            results = permute_prompt(prompt)

            if json_output:
                _output_json(results)
            else:
                for i, result in enumerate(results, 1):
                    if len(results) > 1:
                        console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(result)))

            return results

        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
            else:
                _handle_error(console, error)
            return None

    def json(
        self,
        prompt: str,
        *,
        json_output: bool = True,
        no_color: bool = False,
    ) -> Any | None:
        """
        Parse a prompt into MidjargonDict format.

        Args:
            prompt: The prompt string to parse.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"

        Returns:
            Parsed prompt data if successful, None if error occurs.
        """
        console = Console(force_terminal=not no_color)

        try:
            # Always expand permutations to ensure consistent behavior with other commands
            results = parse_prompt(prompt, permute=True)

            # If there are no permutations (result is a single-item list), return just the dict
            if isinstance(results, list) and len(results) == 1:
                results = results[0]

            # Add computed fields for aspect ratio
            if isinstance(results, list):
                for result in results:
                    if "aspect_width" in result and "aspect_height" in result:
                        result["aspect"] = (
                            f"{result['aspect_width']}:{result['aspect_height']}"
                        )
            elif (
                isinstance(results, dict)
                and "aspect_width" in results
                and "aspect_height" in results
            ):
                results["aspect"] = (
                    f"{results['aspect_width']}:{results['aspect_height']}"
                )

            if json_output:
                _output_json(results)
            else:
                if isinstance(results, list):
                    for i, result in enumerate(results, 1):
                        if len(results) > 1:
                            console.print(f"\nVariant {i}:", style="bold blue")
                        console.print(Panel(_format_prompt(result)))
                else:
                    console.print(Panel(_format_prompt(results)))

            return results

        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
            else:
                _handle_error(console, error)
            return None

    def mj(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> Any | None:
        """
        Convert a prompt to Midjourney format.

        Args:
            prompt: The prompt string to convert.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"

        Returns:
            Converted prompt data if successful, None if error occurs.
        """
        console = Console(force_terminal=not no_color)

        try:
            results = to_midjourney_prompts(prompt)

            # Always wrap single results in a list for consistent handling
            if not isinstance(results, list):
                results = [results]

            # Convert to dictionaries for output and add computed fields
            output_data = []
            for prompt_obj in results:
                if isinstance(prompt_obj, MidjourneyPrompt):
                    data = prompt_obj.model_dump()
                    # Add computed fields
                    if "aspect_width" in data and "aspect_height" in data:
                        data["aspect"] = (
                            f"{data['aspect_width']}:{data['aspect_height']}"
                        )
                    output_data.append(data)
                else:
                    output_data.append(prompt_obj)

            if json_output:
                _output_json(output_data)
            else:
                for i, result in enumerate(results, 1):
                    if len(results) > 1:
                        console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(result)))

            return output_data

        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
            else:
                _handle_error(console, error)
            return None

    def fal(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> Any | None:
        """
        Convert a prompt to Fal.ai format.

        Args:
            prompt: The prompt string to convert.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.

        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"

        Returns:
            Converted prompt data if successful, None if error occurs.
        """
        console = Console(force_terminal=not no_color)

        try:
            results = to_fal_dicts(prompt)

            if json_output:
                _output_json(results)
            else:
                if isinstance(results, list):
                    for i, result in enumerate(results, 1):
                        if len(results) > 1:
                            console.print(f"\nVariant {i}:", style="bold blue")
                        console.print(Panel(_format_prompt(result)))
                else:
                    console.print(Panel(_format_prompt(results)))

            return results

        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
            else:
                _handle_error(console, error)
            return None


def main() -> None:
    fire.Fire(MidjargonCLI())


if __name__ == "__main__":
    main()
