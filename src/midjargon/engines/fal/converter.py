"""
Functions for converting MidjargonDict to Fal.ai API format.
"""

from typing import Any, TypeAlias, cast

from midjargon.core.type_defs import MidjargonDict

# Type alias for Fal.ai API dict format
FalDict: TypeAlias = dict[str, Any]


def _convert_aspect_ratio(d: dict | FalDict | MidjargonDict) -> dict:
    return {
        ("aspect_ratio" if key == "aspect" else key): value for key, value in d.items()
    }


def _convert_image_prompts(d: dict | FalDict | MidjargonDict) -> dict:
    if "images" in d and isinstance(d["images"], list) and d["images"]:
        d["image_url"] = d["images"][0]
        if len(d["images"]) > 1:
            d["_"] = cast(Any, {"images": d["images"][1:]})
        del d["images"]
    return d


def _convert_text_prompt(d: dict | FalDict | MidjargonDict) -> dict:
    return {("prompt" if key == "text" else key): value for key, value in d.items()}


def _convert_numeric_values(d: dict | FalDict | MidjargonDict) -> dict:
    # Transform the dict, performing a conservative conversion of the values to ints or floats where possible (where the values LOOK like ints or floats)
    return {
        key: int(value)
        if str(value).isdigit()
        else float(value)
        if str(value).replace(".", "").isdigit()
        else value
        for key, value in d.items()
    }


def to_fal_dict(d: dict | FalDict | MidjargonDict) -> FalDict:
    for conversion_step in (
        _convert_numeric_values,
        _convert_aspect_ratio,
        _convert_image_prompts,
        _convert_text_prompt,
    ):
        d = conversion_step(d)
    return d
