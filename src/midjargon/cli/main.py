#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///
# this_file: src/midjargon/cli/main.py
"""
midjargon.cli.main
~~~~~~~~~~~~~~~~~~

CLI tool for parsing, permuting, and converting Midjourney prompts.
"""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Any, NoReturn

import fire
from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt_to_dict
from midjargon.engines.fal import to_fal_dict
from midjargon.engines.midjourney import MidjourneyParser
from rich.console import Console
from rich.panel import Panel

if TYPE_CHECKING:
    from midjargon.core.type_defs import MidjargonDict


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _output_json(data: Any) -> None:
    """Write *data* as indented JSON to stdout (no Rich formatting)."""
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.flush()


def _format_prompt(prompt: Any) -> str:
    if hasattr(prompt, "model_dump"):
        return json.dumps(prompt.model_dump(), indent=2)
    return json.dumps(prompt, indent=2)


def _handle_error(console: Console, error: Exception) -> NoReturn:
    error_console = Console(stderr=True)
    error_console.print(f"Error: {error!s}", style="red")
    sys.exit(1)


def permute_prompt(prompt: str) -> list[str]:
    """Expand permutation groups in *prompt*; return list of variant strings."""
    return expand_midjargon_input(prompt)


def parse_prompt(prompt: str, *, permute: bool = True) -> list[MidjargonDict]:
    """Parse *prompt* into a list of ``MidjargonDict`` objects.

    When *permute* is True (default) all ``{…}`` groups are expanded first.
    """
    variants = expand_midjargon_input(prompt) if permute else [prompt]
    return [parse_midjargon_prompt_to_dict(v) for v in variants]


def to_midjourney_prompts(prompt: str) -> list[dict[str, Any]]:
    """Expand + parse *prompt* into serialisable Midjourney prompt dicts."""
    parser = MidjourneyParser()
    results = []
    for variant in expand_midjargon_input(prompt):
        d = parse_midjargon_prompt_to_dict(variant)
        # Rename "images" → "image_prompts" for MidjourneyParser
        if "images" in d:
            d["image_prompts"] = d.pop("images")  # type: ignore[assignment]
        mj = parser.parse_dict(d)
        results.append(mj.model_dump())
    return results


def to_fal_dicts(prompt: str) -> list[dict[str, Any]]:
    """Expand + parse *prompt* and convert each variant to Fal.ai format."""
    results = []
    for variant in expand_midjargon_input(prompt):
        d = parse_midjargon_prompt_to_dict(variant)
        results.append(to_fal_dict(d))
    return results


# ---------------------------------------------------------------------------
# CLI class
# ---------------------------------------------------------------------------

class MidjargonCLI:
    """Midjargon CLI — parse and convert Midjourney-style prompts."""

    def perm(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """Expand all ``{option1, option2}`` permutation groups.

        Args:
            prompt: Raw prompt string, e.g. ``"a {red, blue} bird"``.
            json_output: Output as JSON array of strings.
            no_color: Disable ANSI colour output.
        """
        console = Console(force_terminal=not no_color)
        try:
            results = permute_prompt(prompt)
            if json_output:
                _output_json(results)
                return
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                console.print(Panel(result))
        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def json(
        self,
        prompt: str,
        *,
        json_output: bool = True,
        no_color: bool = False,
    ) -> None:
        """Parse a prompt into ``MidjargonDict`` format (flat parameter dict).

        Permutation groups are expanded automatically.  A single-variant
        prompt returns a dict; a multi-variant prompt returns a list.

        Args:
            prompt: Raw prompt string.
            json_output: Output as JSON (default True).
            no_color: Disable ANSI colour output.
        """
        console = Console(force_terminal=not no_color)
        try:
            results = parse_prompt(prompt, permute=True)
            # Single variant → return plain dict
            output: Any = results[0] if len(results) == 1 else results
            if json_output:
                _output_json(output)
                return
            if isinstance(output, list):
                for i, item in enumerate(output, 1):
                    console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(item)))
            else:
                console.print(Panel(_format_prompt(output)))
        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def mj(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """Convert a prompt to validated Midjourney format.

        Args:
            prompt: Raw prompt string.
            json_output: Output as JSON.
            no_color: Disable ANSI colour output.
        """
        console = Console(force_terminal=not no_color)
        try:
            results = to_midjourney_prompts(prompt)
            output: Any = results[0] if len(results) == 1 else results
            if json_output:
                _output_json(output)
                return
            if isinstance(output, list):
                for i, item in enumerate(output, 1):
                    console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(item)))
            else:
                console.print(Panel(_format_prompt(output)))
        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)

    def fal(
        self,
        prompt: str,
        *,
        json_output: bool = False,
        no_color: bool = False,
    ) -> None:
        """Convert a prompt to Fal.ai API format.

        Args:
            prompt: Raw prompt string.
            json_output: Output as JSON.
            no_color: Disable ANSI colour output.
        """
        console = Console(force_terminal=not no_color)
        try:
            results = to_fal_dicts(prompt)
            output: Any = results[0] if len(results) == 1 else results
            if json_output:
                _output_json(output)
                return
            if isinstance(output, list):
                for i, item in enumerate(output, 1):
                    console.print(f"\nVariant {i}:", style="bold blue")
                    console.print(Panel(_format_prompt(item)))
            else:
                console.print(Panel(_format_prompt(output)))
        except (ValueError, TypeError, SyntaxError) as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.exit(1)
            else:
                _handle_error(console, error)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the Midjargon CLI."""
    from rich.ansi import AnsiDecoder
    from rich.console import Console, Group
    from rich.theme import Theme
    from rich.traceback import install

    install(show_locals=True)
    ansi_decoder = AnsiDecoder()
    console = Console(theme=Theme({"prompt": "cyan", "question": "bold cyan"}))

    def display(lines: Any, out: Any) -> None:
        console.print(Group(*map(ansi_decoder.decode_line, lines)))

    fire.core.Display = display
    fire.Fire(MidjargonCLI())


if __name__ == "__main__":
    main()
