#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/midjourney.py
from __future__ import annotations

from typing import Any

from midjargon.core.models import (CharacterReference, ImageReference,
                                   MidjourneyParameters, MidjourneyPrompt,
                                   StyleReference)
from pydantic import HttpUrl


class MidjourneyParser:
    """Parser for converting between Midjourney prompt formats."""

    def _parse_url(self, url: str) -> HttpUrl:
        """Parse a URL string into an HttpUrl object.

        Args:
            url: URL string to parse.

        Returns:
            HttpUrl instance.
        """
        return HttpUrl(url)

    def parse_dict(self, prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt.

        Args:
            prompt_dict: Dictionary containing prompt data.

        Returns:
            MidjourneyPrompt instance.

        Raises:
            ValueError: If the prompt text is empty.
        """
        # Validate text
        text = prompt_dict.pop("text", "").strip()
        if not text:
            msg = "Empty prompt"
            raise ValueError(msg)

        # Handle image prompts
        image_prompts = []
        raw_image_prompts = prompt_dict.pop("image_prompts", [])
        for img in raw_image_prompts:
            if isinstance(img, str):
                image_prompts.append(ImageReference(url=self._parse_url(img)))
            elif isinstance(img, dict):
                if "url" in img and isinstance(img["url"], str):
                    img["url"] = self._parse_url(img["url"])
                image_prompts.append(ImageReference(**img))
            elif isinstance(img, ImageReference):
                image_prompts.append(img)

        # Handle parameters
        params = MidjourneyParameters()

        # Handle aspect ratio
        if "ar" in prompt_dict:
            params.aspect_ratio = prompt_dict.pop("ar")
        elif "aspect_ratio" in prompt_dict:
            params.aspect_ratio = prompt_dict.pop("aspect_ratio")
        elif "aspect" in prompt_dict:
            params.aspect_ratio = prompt_dict.pop("aspect")
        elif all(k in prompt_dict for k in ["aspect_width", "aspect_height"]):
            params.aspect_width = int(prompt_dict.pop("aspect_width"))
            params.aspect_height = int(prompt_dict.pop("aspect_height"))

        # Handle version
        if "v" in prompt_dict:
            params.version = prompt_dict.pop("v")
        elif "version" in prompt_dict:
            params.version = prompt_dict.pop("version")

        # Handle style
        if "style" in prompt_dict:
            params.style = prompt_dict.pop("style")

        # Handle numeric parameters
        if "s" in prompt_dict:
            params.stylize = float(prompt_dict.pop("s"))
        elif "stylize" in prompt_dict:
            params.stylize = float(prompt_dict.pop("stylize"))

        if "c" in prompt_dict:
            params.chaos = float(prompt_dict.pop("c"))
        elif "chaos" in prompt_dict:
            params.chaos = float(prompt_dict.pop("chaos"))

        if "weird" in prompt_dict:
            params.weird = float(prompt_dict.pop("weird"))

        if "seed" in prompt_dict:
            params.seed = prompt_dict.pop("seed")

        # Handle boolean flags
        for flag in ["tile", "turbo", "relax", "personalization"]:
            if flag in prompt_dict:
                setattr(params, flag, bool(prompt_dict.pop(flag)))

        # Handle references
        if "cref" in prompt_dict:
            ref = prompt_dict.pop("cref")
            weight = float(prompt_dict.pop("cw", 1.0))
            if isinstance(ref, str):
                if ref.startswith("http"):
                    params.character_reference.append(
                        CharacterReference(url=self._parse_url(ref), weight=weight)
                    )
                else:
                    params.character_reference.append(
                        CharacterReference(code=ref, weight=weight)
                    )

        if "sref" in prompt_dict:
            ref = prompt_dict.pop("sref")
            weight = float(prompt_dict.pop("sw", 1.0))
            if isinstance(ref, str):
                if ref.startswith("http"):
                    params.style_reference.append(
                        StyleReference(url=self._parse_url(ref), weight=weight)
                    )
                else:
                    params.style_reference.append(
                        StyleReference(code=ref, weight=weight)
                    )

        # Handle remaining parameters
        params.extra_params = prompt_dict

        return MidjourneyPrompt(
            text=text,
            image_prompts=image_prompts,
            parameters=params,
        )


def parse_midjourney_dict(prompt_dict: dict[str, Any]) -> MidjourneyPrompt:
    """Convert a dictionary to a MidjourneyPrompt.

    Args:
        prompt_dict: Dictionary containing prompt data.

    Returns:
        MidjourneyPrompt instance.
    """
    parser = MidjourneyParser()
    return parser.parse_dict(prompt_dict)
