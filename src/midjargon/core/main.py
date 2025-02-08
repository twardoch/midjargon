# this_file: src/midjargon/core/main.py

from typing import Any

from midjargon.core.models import PromptVariant


def format_json_output(
    variants: list[PromptVariant], include_parsed: bool = False
) -> dict[str, Any]:
    """Format prompt variants as JSON output.

    Args:
        variants: List of prompt variants to format.
        include_parsed: Whether to include parsed data in output.

    Returns:
        Dictionary containing formatted output.
    """
    if not variants:
        return {}

    # For single variants without weights, return simple format
    if len(variants) == 1 and variants[0].weight == 1.0:
        variant = variants[0].prompt
        result = {
            "text": variant.text,
            "images": [str(img.url) for img in variant.images],
            "parameters": variant.parameters.model_dump(exclude_none=True),
        }
        if include_parsed:
            result["parsed"] = variant.model_dump(exclude_none=True)
        return result

    # For multiple variants or weighted variants, return array format
    results = []
    for variant in variants:
        prompt = variant.prompt
        result = {
            "text": prompt.text,
            "images": [str(img.url) for img in prompt.images],
            "parameters": prompt.parameters.model_dump(exclude_none=True),
            "weight": variant.weight,
        }
        if include_parsed:
            result["parsed"] = prompt.model_dump(exclude_none=True)
        results.append(result)
    return {"variants": results}
