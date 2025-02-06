"""
Parser for Midjourney engine.
"""

from typing import Any, cast

from midjargon.engines.base import EngineParser

from ...core.type_defs import MidjargonDict
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
            ("stylize", "s"): ("stylize", lambda v: int(v) if v else None),
            ("chaos", "c"): ("chaos", lambda v: int(v) if v else None),
            ("weird",): ("weird", lambda v: int(v) if v else None),
            ("iw",): ("image_weight", lambda v: float(v) if v else None),
            ("seed",): ("seed", lambda v: int(v) if v else None),
            ("stop",): ("stop", lambda v: int(v) if v else None),
            ("quality", "q"): ("quality", lambda v: float(v) if v else None),
            ("repeat", "r"): ("repeat", lambda v: int(v) if v else None),
            ("character_weight", "cw"): (
                "character_weight",
                lambda v: int(v) if v else None,
            ),
            ("style_weight", "sw"): ("style_weight", lambda v: int(v) if v else None),
            ("style_version", "sv"): ("style_version", lambda v: int(v) if v else None),
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
        elif name == "v" or name == "version":
            if not value:
                return "version", None
            return "version", value if value.startswith("v") else f"v{value}"
        elif name == "niji":
            if not value:
                return "version", "niji"
            return "version", f"niji {value}"
        elif name == "p" or name == "personalization":
            return "personalization", value if value else ""
        return "", None

    def _handle_reference_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str, list[str]]:
        """Handle reference parameter conversion."""
        if raw_value is None:
            return "", []

        # Convert string to list if needed
        if isinstance(raw_value, str):
            values = raw_value.split(",")
        else:
            values = raw_value

        # Filter out empty strings and strip whitespace
        values = [v.strip() for v in values if v.strip()]

        if name == "cref":
            return "character_reference", values
        elif name == "sref":
            return "style_reference", values
        return "", []

    def _handle_flag_param(self, name: str) -> tuple[str, bool]:
        """Handle flag parameter conversion."""
        flag_map = {
            "turbo": "turbo",
            "relax": "relax",
            "tile": "tile",
        }
        return flag_map.get(name, ""), True

    def _handle_negative_prompt(
        self, raw_value: str | list[str] | None
    ) -> tuple[str, str | None]:
        """Handle negative prompt parameter."""
        if raw_value is None:
            return "negative_prompt", None

        # Convert list to string if needed
        if isinstance(raw_value, list):
            value = ", ".join(raw_value)
        else:
            value = raw_value

        return "negative_prompt", value

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
            "version": None,
            "personalization": None,
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

            # Handle reference parameters
            param_name, param_value = self._handle_reference_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue

            # Handle flag parameters
            if value is None:  # Flag parameter
                param_name, param_value = self._handle_flag_param(name)
                if param_name:
                    prompt_data[param_name] = param_value
                    continue

            # Handle negative prompt
            if name == "no":
                param_name, param_value = self._handle_negative_prompt(value)
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
        if prompt.quality is not None:
            params["quality"] = str(prompt.quality)
        if prompt.repeat is not None:
            params["repeat"] = str(prompt.repeat)
        if prompt.character_weight is not None:
            params["cw"] = str(prompt.character_weight)
        if prompt.style_weight is not None:
            params["sw"] = str(prompt.style_weight)
        if prompt.style_version is not None:
            params["sv"] = str(prompt.style_version)
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

    def _format_reference_params(
        self, prompt: MidjourneyPrompt
    ) -> dict[str, list[str]]:
        """Format reference parameters for dictionary output."""
        params = {}
        if prompt.character_reference:
            params["cref"] = prompt.character_reference
        if prompt.style_reference:
            params["sref"] = prompt.style_reference
        return params

    def _format_flag_params(self, prompt: MidjourneyPrompt) -> dict[str, None]:
        """Format flag parameters for dictionary output."""
        params = {}
        if prompt.turbo:
            params["turbo"] = None
        if prompt.relax:
            params["relax"] = None
        if prompt.tile:
            params["tile"] = None
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

        # Add reference parameters
        result.update(self._format_reference_params(prompt))

        # Add flag parameters
        result.update(self._format_flag_params(prompt))

        # Add negative prompt
        if prompt.negative_prompt is not None:
            result["no"] = prompt.negative_prompt

        # Add extra parameters
        result.update(prompt.extra_params)

        return result

    def parse_midjourney_dict(self, data: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a dictionary into a MidjourneyPrompt object.

        Args:
            data: Dictionary to parse.

        Returns:
            MidjourneyPrompt object.

        Raises:
            ValueError: If data is invalid.
        """
        # Validate text
        text = str(data.get("text", "")).strip()
        if not text:
            msg = "Empty prompt text"
            raise ValueError(msg)

        # Convert image prompts
        raw_image_prompts = data.get("images", [])
        if not isinstance(raw_image_prompts, list):
            raw_image_prompts = [raw_image_prompts]
        image_prompts = [ImagePrompt(url=str(p)) for p in raw_image_prompts if p]

        # Convert integer parameters with defaults
        int_params: dict[str, int | None] = {
            "stylize": None,
            "chaos": None,
            "weird": None,
            "seed": None,
            "stop": None,
            "aspect_width": None,
            "aspect_height": None,
            "character_weight": None,
            "style_weight": None,
            "style_version": None,
            "repeat": None,
        }
        for name, default in int_params.items():
            value = data.get(name)
            if value is not None:
                try:
                    int_params[name] = int(float(str(value)))
                except (ValueError, TypeError):
                    msg = f"Invalid value for {name}: {value}"
                    raise ValueError(msg) from None

        # Convert float parameters
        float_params: dict[str, float | None] = {
            "image_weight": None,
            "quality": None,
        }
        for name, default in float_params.items():
            value = data.get(name)
            if value is not None:
                try:
                    float_params[name] = float(str(value))
                except (ValueError, TypeError):
                    msg = f"Invalid value for {name}: {value}"
                    raise ValueError(msg) from None

        # Convert string parameters
        string_params: dict[str, str | None] = {
            "style": None,
            "version": None,
            "personalization": None,
        }
        for name in string_params:
            value = data.get(name)
            if value is not None:
                string_params[name] = str(value)

        # Convert reference lists
        reference_lists: dict[str, list[str]] = {
            "character_reference": [],
            "style_reference": [],
        }
        for name in reference_lists:
            value = data.get(name, [])
            if not isinstance(value, list):
                value = [str(value)] if value else []
            reference_lists[name] = [str(v) for v in value if v]

        # Convert boolean flags
        boolean_flags: dict[str, bool] = {
            "turbo": False,
            "relax": False,
            "tile": False,
        }
        for name in boolean_flags:
            value = data.get(name)
            if value is not None:
                if isinstance(value, str):
                    boolean_flags[name] = value.lower() == "true"
                else:
                    boolean_flags[name] = bool(value)

        # Get extra parameters
        extra_params = data.get("extra_params", {})
        if not isinstance(extra_params, dict):
            extra_params = {}

        # Handle negative prompt
        negative_prompt = data.get("negative_prompt")
        if negative_prompt is not None:
            negative_prompt = str(negative_prompt)

        # Create prompt object with explicit parameter groups
        return MidjourneyPrompt(
            text=text,
            image_prompts=image_prompts,
            negative_prompt=negative_prompt,
            extra_params=extra_params,
            stylize=int_params["stylize"],
            chaos=int_params["chaos"],
            weird=int_params["weird"],
            image_weight=float_params["image_weight"],
            seed=int_params["seed"],
            stop=int_params["stop"],
            aspect_width=int_params["aspect_width"],
            aspect_height=int_params["aspect_height"],
            style=string_params["style"],
            version=string_params["version"],
            personalization=string_params["personalization"],
            quality=float_params["quality"],
            character_reference=reference_lists["character_reference"],
            style_reference=reference_lists["style_reference"],
            character_weight=int_params["character_weight"],
            style_weight=int_params["style_weight"],
            style_version=int_params["style_version"],
            repeat=int_params["repeat"],
            turbo=boolean_flags["turbo"],
            relax=boolean_flags["relax"],
            tile=boolean_flags["tile"],
        )
