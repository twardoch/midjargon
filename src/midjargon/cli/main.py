#!/usr/bin/env -S uv run
# this_file: src/midjargon/cli/main.py
# /// script
# dependencies = ["fire", "rich"]
# ///

import json
import sys
from typing import Any, Sequence

import fire
from rich.console import Console

from midjargon.core.input import expand_midjargon_input
from midjargon.core.models import PromptVariant
from midjargon.engines.midjourney import MidjourneyParser

# Set up console for output
console = Console()
error_console = Console(stderr=True)


def format_json_output(variants: Sequence[PromptVariant]) -> dict[str, Any]:
    """Format variants as JSON output."""
    return {"variants": [variant.prompt.model_dump() for variant in variants]}


def format_rich_output(variants: Sequence[PromptVariant]) -> str:
    """Format variants as rich text output."""
    if len(variants) == 1:
        return variants[0].prompt.to_string()
    return "\n".join(f"{i + 1}. {v.prompt.to_string()}" for i, v in enumerate(variants))


class MidjargonCLI:
    """CLI interface for midjargon."""

    def json(self, prompt: str) -> None:
        """Parse a prompt to MidjargonDict format.

        Args:
            prompt: The prompt to parse.
        """
        try:
            variants = expand_midjargon_input(prompt)
            output = format_json_output(variants)
            print(json.dumps(output))
        except Exception as e:
            error_console.print(f"[red]Error:[/red] {e!s}")
            sys.exit(1)

    def mj(self, prompt: str, json_output: bool = False) -> None:
        """Convert a prompt to Midjourney format.

        Args:
            prompt: The prompt to convert.
            json_output: Whether to output JSON.
        """
        try:
            variants = expand_midjargon_input(prompt)
            parser = MidjourneyParser()
            results = []
            for variant in variants:
                mj_prompt = parser.parse_dict(variant.prompt.model_dump())
                results.append(mj_prompt.model_dump())

            if json_output:
                print(json.dumps({"variants": results}))
            else:
                for i, result in enumerate(results):
                    if len(results) > 1:
                        console.print(f"{i + 1}. ", end="")
                    console.print(
                        f"{result['text']} {' '.join(f'--{k} {v}' for k, v in result.items() if k != 'text' and v is not None)}"
                    )
        except Exception as e:
            error_console.print(f"[red]Error:[/red] {e!s}")
            sys.exit(1)

    def perm(self, prompt: str, json_output: bool = False) -> None:
        """Expand permutations in a prompt.

        Args:
            prompt: The prompt to expand.
            json_output: Whether to output JSON.
        """
        try:
            variants = expand_midjargon_input(prompt)
            if json_output:
                output = format_json_output(variants)
                print(json.dumps(output))
            else:
                print(format_rich_output(variants))
        except Exception as e:
            error_console.print(f"[red]Error:[/red] {e!s}")
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    try:
        fire.Fire(MidjargonCLI)
    except Exception as e:
        error_console.print(f"[red]Error:[/red] {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
