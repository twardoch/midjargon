"""
Parser for Midjourney engine.
"""

from typing import Any

from midjargon.core.type_defs import MidjargonDict
from midjargon.engines.base import EngineParser
from .models import ImagePrompt, MidjourneyPrompt


class MidjourneyParser(EngineParser[MidjourneyPrompt]):
    """Parser for Midjourney prompts."""

    def _handle_numeric_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str, Any]:
        """Handle numeric parameter conversion."""
        # Handle p parameter separately since it can be a string or None
        if name == "p":
            return "personalization", raw_value if isinstance(raw_value, str) else None

        # Convert list to string if needed
        if raw_value is None:
            value = None
        elif isinstance(raw_value, list):
            value = raw_value[0]
        else:
            value = raw_value

        # Define parameter mappings with their default values and conversion functions
        param_map = {
            ("stylize", "s"): ("stylize", lambda v: int(v) if v else 100),
            ("chaos", "c"): ("chaos", lambda v: int(v) if v else 0),
            ("weird",): ("weird", lambda v: int(v) if v else 0),
            ("iw",): ("image_weight", lambda v: float(v) if v else 1.0),
            ("seed",): ("seed", lambda v: int(v) if v else None),
            ("stop",): ("stop", lambda v: int(v) if v else 100),
        }

        # Find matching parameter and convert value
        for aliases, (param_name, converter) in param_map.items():
            if name in aliases:
                return param_name, converter(value)

        return "", None

    def _handle_aspect_ratio(
        self, raw_value: str | list[str] | None
    ) -> tuple[int | None, int | None]:
        """Handle aspect ratio parameter conversion."""
        # Convert list to string if needed
        if raw_value is None:
            value = None
        elif isinstance(raw_value, list):
            value = raw_value[0]
        else:
            value = raw_value

        if not value:
            return None, None
        try:
            w, h = value.split(":")
            return int(w), int(h)
        except ValueError as e:
            msg = "Invalid aspect ratio format. Expected w:h"
            raise ValueError(msg) from e

    def _handle_style_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str, str | None]:
        """Handle style parameter conversion."""
        # Convert list to string if needed
        if raw_value is None:
            value = None
        elif isinstance(raw_value, list):
            value = raw_value[0]
        else:
            value = raw_value

        if name == "style":
            return "style", value
        elif name == "v":
            return "version", f"v{value}" if value else None
        elif name == "niji":
            return "version", f"niji {value}" if value else "niji"
        return "", None

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.

        Args:
            midjargon_dict: Dictionary from basic parser.

        Returns:
            Validated MidjourneyPrompt.
        """
        # Initialize with core components
        images = midjargon_dict.get("images", [])
        if images is None:
            images = []

        prompt_data: dict[str, Any] = {
            "text": midjargon_dict["text"],
            "image_prompts": [ImagePrompt(url=url) for url in images],
            "extra_params": {},
        }

        # Process each parameter
        for name, value in midjargon_dict.items():
            if name in ("text", "images"):
                continue

            # Try numeric parameters first
            param_name, param_value = self._handle_numeric_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue

            # Handle aspect ratio
            if name in ("ar", "aspect"):
                w, h = self._handle_aspect_ratio(value)
                if w is not None and h is not None:
                    prompt_data["aspect_width"] = w
                    prompt_data["aspect_height"] = h
                continue

            # Handle style parameters
            param_name, param_value = self._handle_style_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue

            # Store unknown parameters
            if isinstance(value, list):
                prompt_data["extra_params"][name] = value[0]
            else:
                prompt_data["extra_params"][name] = value

        return MidjourneyPrompt(**prompt_data)

    def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format numeric parameters for dictionary output."""
        params = {}
        if prompt.stylize is not None:
            params["stylize"] = str(prompt.stylize)
        if prompt.chaos is not None:
            params["chaos"] = str(prompt.chaos)
        if prompt.weird is not None:
            params["weird"] = str(prompt.weird)
        if prompt.image_weight is not None:
            params["iw"] = str(prompt.image_weight)
        if prompt.seed is not None:
            params["seed"] = str(prompt.seed)
        if prompt.stop is not None:
            params["stop"] = str(prompt.stop)
        return params

    def _format_style_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format style parameters for dictionary output."""
        params = {}
        if prompt.style is not None:
            params["style"] = prompt.style
        if prompt.version is not None:
            if prompt.version.startswith("niji"):
                params["niji"] = prompt.version[5:].strip()
            else:
                params["v"] = prompt.version[1:]
        if prompt.personalization is not None:
            params["p"] = prompt.personalization
        return params

    def _format_aspect_ratio(
        self, width: int | None, height: int | None
    ) -> dict[str, str]:
        """Format aspect ratio for dictionary output."""
        if width is not None and height is not None:
            return {"ar": f"{width}:{height}"}
        return {}

    def to_dict(self, prompt: MidjourneyPrompt) -> dict[str, Any]:
        """
        Convert a MidjourneyPrompt back to a dictionary.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary representation.
        """
        result: dict[str, Any] = {
            "text": prompt.text,
            "images": [p.url for p in prompt.image_prompts],
        }

        # Add numeric parameters
        result.update(self._format_numeric_params(prompt))

        # Add aspect ratio
        result.update(
            self._format_aspect_ratio(prompt.aspect_width, prompt.aspect_height)
        )

        # Add style parameters
        result.update(self._format_style_params(prompt))

        # Add extra parameters
        result.update(prompt.extra_params)

        return result
