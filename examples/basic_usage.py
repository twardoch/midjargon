#!/usr/bin/env python3
# this_file: examples/basic_usage.py

"""
Example script demonstrating basic usage of the midjargon package.
"""

from rich.console import Console
from rich.panel import Panel

from midjargon.core.input import expand_midjargon_input
from midjargon.core.parser import parse_midjargon_prompt

console = Console()


def main():
    # Example 1: Basic prompt parsing
    console.print("\n[bold blue]Example 1: Basic Prompt[/]")
    prompt = "a beautiful landscape --ar 16:9 --stylize 200"
    result = parse_midjargon_prompt(prompt)
    console.print(
        Panel(
            f"Text: {result.text}\n"
            f"Aspect Ratio: {result.parameters.aspect}\n"
            f"Stylize: {result.parameters.stylize}"
        )
    )

    # Example 2: Using image references
    console.print("\n[bold blue]Example 2: Image Reference[/]")
    prompt = "https://example.com/image.jpg a photo in this style --stylize 100"
    result = parse_midjargon_prompt(prompt)
    console.print(
        Panel(
            f"Text: {result.text}\n"
            f"Image URL: {result.images[0].url if result.images else 'None'}\n"
            f"Stylize: {result.parameters.stylize}"
        )
    )

    # Example 3: Permutations
    console.print("\n[bold blue]Example 3: Permutations[/]")
    prompt = "a {red, blue} bird on a {green, yellow} tree"
    variants = expand_midjargon_input(prompt)
    for i, variant in enumerate(variants, 1):
        console.print(f"Variant {i}: {variant.prompt.text}")

    # Example 4: Weighted prompts
    console.print("\n[bold blue]Example 4: Weighted Prompts[/]")
    prompt = "first style::0.7 second style::0.3"
    variants = expand_midjargon_input(prompt)
    for variant in variants:
        console.print(Panel(f"Text: {variant.prompt.text}\nWeight: {variant.weight}"))

    # Example 5: Style references
    console.print("\n[bold blue]Example 5: Style References[/]")
    prompt = "test --sref p123456 --sw 200"
    result = parse_midjargon_prompt(prompt)
    if result.parameters.style_reference:
        console.print(
            Panel(
                f"Text: {result.text}\n"
                f"Style Code: {result.parameters.style_reference.code}\n"
                f"Weight: {result.parameters.style_reference.weight}"
            )
        )

    # Example 6: Combined features
    console.print("\n[bold blue]Example 6: Combined Features[/]")
    prompt = "a {vintage, modern} {portrait, landscape}::0.6 another style::0.4"
    variants = expand_midjargon_input(prompt)
    console.print(f"Total variants: {len(variants)}")
    for i, variant in enumerate(variants, 1):
        console.print(
            Panel(
                f"Variant {i}:\nText: {variant.prompt.text}\nWeight: {variant.weight}"
            )
        )


if __name__ == "__main__":
    main()
