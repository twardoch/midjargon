"""
Parser for Midjourney engine.
"""

from typing import Any

from midjargon.core.type_defs import MidjargonDict
from midjargon.engines.base import EngineParser

from .constants import (
    CHAOS_RANGE,
    CHARACTER_WEIGHT_RANGE,
    IMAGE_WEIGHT_RANGE,
    QUALITY_RANGE,
    REPEAT_RANGE,
    SEED_RANGE,
    STOP_RANGE,
    STYLE_VERSION_RANGE,
    STYLE_WEIGHT_RANGE,
    STYLIZE_RANGE,
    VALID_NIJI_VERSIONS,
    VALID_VERSIONS,
    WEIRD_RANGE,
)
from .models import ImagePrompt, MidjourneyPrompt


class MidjourneyParser(EngineParser[MidjourneyPrompt]):
    """Parser for Midjourney prompts."""

    def _normalize_value(self, value: str | list[str] | None) -> str | list[str] | None:
        """Convert a parameter value to a normalized string or list."""
        if value is None:
            return None
        if isinstance(value, list):
            return value if value else None
        return value

    def _validate_numeric_range(self, name: str, value: int | float) -> None:
        """Validate numeric value is within allowed range."""
        ranges = {
            "stylize": STYLIZE_RANGE,
            "chaos": CHAOS_RANGE,
            "weird": WEIRD_RANGE,
            "image_weight": IMAGE_WEIGHT_RANGE,
            "seed": SEED_RANGE,
            "stop": STOP_RANGE,
            "quality": QUALITY_RANGE,
            "character_weight": CHARACTER_WEIGHT_RANGE,
            "style_weight": STYLE_WEIGHT_RANGE,
            "style_version": STYLE_VERSION_RANGE,
            "repeat": REPEAT_RANGE,
        }

        if name in ranges:
            min_val, max_val = ranges[name]
            if not min_val <= value <= max_val:
                msg = (
                    f"Value {value} for {name} must be between {min_val} and {max_val}"
                )
                raise ValueError(msg)

    def _get_normalized_name(self, name: str) -> str:
        """Get normalized parameter name from shorthand."""
        name_map = {
            "s": "stylize",
            "c": "chaos",
            "w": "weird",
            "iw": "image_weight",
            "q": "quality",
            "cw": "character_weight",
            "sw": "style_weight",
            "sv": "style_version",
            "r": "repeat",
        }
        return name_map.get(name, name)

    def _convert_numeric_value(
        self, name: str, value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Convert and validate numeric value."""
        if value is None:
            return None, None

        if isinstance(value, list):
            value = value[0] if value else None
            if value is None:
                return None, None

        try:
            # Define parameter types and their validation functions
            param_types = {
                "stylize": (int, lambda x: self._validate_numeric_range("stylize", x)),
                "chaos": (int, lambda x: self._validate_numeric_range("chaos", x)),
                "weird": (int, lambda x: self._validate_numeric_range("weird", x)),
                "image_weight": (
                    float,
                    lambda x: self._validate_numeric_range("image_weight", x),
                ),
                "quality": (
                    float,
                    lambda x: self._validate_numeric_range("quality", x),
                ),
                "character_weight": (
                    float,
                    lambda x: self._validate_numeric_range("character_weight", x),
                ),
                "style_weight": (
                    float,
                    lambda x: self._validate_numeric_range("style_weight", x),
                ),
                "style_version": (
                    int,
                    lambda x: self._validate_numeric_range("style_version", x),
                ),
                "repeat": (int, lambda x: self._validate_numeric_range("repeat", x)),
            }

            if name in param_types and isinstance(value, str):
                type_func, validate_func = param_types[name]
                val = type_func(value)
                validate_func(val)
                return name, val

            return None, None

        except (ValueError, TypeError):
            return None, None

    def _handle_numeric_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle numeric parameter conversion."""
        value = self._normalize_value(raw_value)
        if value is None:
            return None, None

        # Get normalized parameter name
        name = self._get_normalized_name(name)

        # Convert and validate the value
        return self._convert_numeric_value(name, value)

    def _handle_aspect_ratio(
        self, raw_value: str | list[str] | None
    ) -> tuple[int | None, int | None]:
        """Handle aspect ratio parameter conversion."""
        value = self._normalize_value(raw_value)
        if value is None:
            return None, None

        # Convert value to string if it's a list
        if isinstance(value, list):
            value = value[0] if value else None
            if value is None:
                return None, None

        try:
            width_str, height_str = value.split(":")
            width = int(width_str)
            height = int(height_str)
            return width, height
        except (ValueError, AttributeError) as e:
            msg = f"Invalid aspect ratio format: {value}"
            raise ValueError(msg) from e

    def _handle_style_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle style parameter conversion."""
        if name != "style":
            return None, None
        value = self._normalize_value(raw_value)
        if value is None:
            return None, None
        if isinstance(value, list):
            new_value = value[0] if value else None
            if new_value is None or not isinstance(new_value, str):
                return None, None
        else:
            if not isinstance(value, str):
                return None, None
            new_value = value
        # new_value is now guaranteed to be a string
        return "style", new_value

    def _handle_version_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle version parameter conversion."""
        value = self._normalize_value(raw_value)
        if value is None:
            if name == "niji":
                return "version", "niji"
            return None, None
        if isinstance(value, list):
            new_value = value[0] if value else None
        else:
            new_value = value

        # If new_value already starts with 'niji', return it as is
        if isinstance(new_value, str) and new_value.lower().startswith("niji"):
            # Validate niji version
            parts = new_value.split()
            if len(parts) > 1 and parts[1] not in VALID_NIJI_VERSIONS:
                msg = f"Invalid niji version: {parts[1]}"
                raise ValueError(msg)
            return "version", new_value

        if name == "niji":
            # Validate niji version
            if new_value and str(new_value) not in VALID_NIJI_VERSIONS:
                msg = f"Invalid niji version: {new_value}"
                raise ValueError(msg)
            return "version", f"niji {new_value}" if new_value else "niji"

        if name in ("v", "version"):
            # Strip 'v' prefix if present for validation
            version_str = str(new_value)
            if version_str.startswith("v"):
                version_str = version_str[1:]
            # Validate version number
            if not version_str or version_str not in VALID_VERSIONS:
                msg = f"Invalid version: {new_value}"
                raise ValueError(msg)
            return "version", f"v{version_str}"

        return None, None

    def _handle_personalization_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle personalization parameter conversion."""
        if name not in ("p", "personalization"):
            return None, None

        value = self._normalize_value(raw_value)
        if value is None:
            return "personalization", None

        if isinstance(value, list):
            new_value = value[0] if value else None
            if new_value is None:
                return "personalization", None
        else:
            new_value = value

        return "personalization", str(new_value)

    def _handle_negative_prompt(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle negative prompt parameter conversion only if name is 'negative_prompt'."""
        if name != "negative_prompt":
            return None, None
        value = self._normalize_value(raw_value)
        if value is None:
            return None, None
        if isinstance(value, list):
            value = value[0] if value else None
            if value is None:
                return None, None
        return "negative_prompt", value

    def _handle_reference_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, list[str] | None]:
        """Handle reference parameter conversion."""
        value = self._normalize_value(raw_value)
        if value is None:
            return None, None

        # Handle shorthand names
        name_map = {
            "cref": "character_reference",
            "sref": "style_reference",
        }
        name = name_map.get(name, name)

        # Only validate extensions for reference parameters
        if name in ["character_reference", "style_reference"]:
            # Convert value to list if needed
            if isinstance(value, str):
                value = [value]

            # Validate file extensions
            for ref in value:
                if not any(
                    ref.lower().endswith(ext)
                    for ext in (".jpg", ".jpeg", ".png", ".gif")
                ):
                    msg = f"Invalid reference file extension for {name}: {ref}"
                    raise ValueError(msg)

            return name, value

        return None, None

    def _get_default_prompt_data(self) -> dict[str, Any]:
        """Get default prompt data structure."""
        return {
            "text": "",
            "image_prompts": [],
            "negative_prompt": None,
            "stylize": None,
            "chaos": None,
            "weird": None,
            "image_weight": None,
            "seed": None,
            "stop": None,
            "quality": None,
            "character_weight": None,
            "style_weight": None,
            "style_version": None,
            "repeat": None,
            "aspect_width": None,
            "aspect_height": None,
            "style": None,
            "version": None,
            "personalization": None,
            "character_reference": [],
            "style_reference": [],
            "turbo": False,
            "relax": False,
            "tile": False,
            "extra_params": {},
        }

    def _process_text_and_images(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process text and image prompts."""
        text = midjargon_dict.get("text", "")
        if not text:
            msg = "Prompt text cannot be empty"
            raise ValueError(msg)
        prompt_data["text"] = text

        # Handle image prompts
        image_prompts = []
        images = midjargon_dict.get("images", [])
        if images is not None:
            for image_url in images:
                image_prompts.append(ImagePrompt(url=image_url))
        prompt_data["image_prompts"] = image_prompts

    def _process_version_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process version parameters."""
        for name, value in midjargon_dict.items():
            if name in ("v", "version"):
                param_name, param_value = self._handle_version_param(name, value)
                if param_name:
                    prompt_data[param_name] = param_value
                    break  # Stop after finding a --v parameter

    def _process_numeric_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process numeric parameters."""
        numeric_params = {
            "s",
            "stylize",
            "c",
            "chaos",
            "w",
            "weird",
            "iw",
            "image_weight",
            "seed",
            "stop",
            "q",
            "quality",
            "cw",
            "character_weight",
            "sw",
            "style_weight",
            "sv",
            "style_version",
            "r",
            "repeat",
        }
        for name, value in midjargon_dict.items():
            if name in numeric_params:
                param_name, param_value = self._handle_numeric_param(name, value)
                if param_name:
                    prompt_data[param_name] = param_value

    def _process_style_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process style parameters."""
        style_params = {"style", "raw"}
        for name, value in midjargon_dict.items():
            if name in style_params:
                param_name, param_value = self._handle_style_param(name, value)
                if param_name:
                    prompt_data[param_name] = param_value

    def _process_aspect_ratio(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process aspect ratio parameters."""
        if "ar" in midjargon_dict:
            width, height = self._handle_aspect_ratio(midjargon_dict["ar"])
            if width is not None and height is not None:
                prompt_data["aspect_width"] = width
                prompt_data["aspect_height"] = height

    def _process_reference_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process reference parameters."""
        for name, value in midjargon_dict.items():
            if name in ("cr", "character_reference", "sr", "style_reference"):
                param_name, param_value = self._handle_reference_param(name, value)
                if param_name and param_value:
                    prompt_data[param_name] = param_value

    def _process_flag_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process flag parameters."""
        flag_params = {"turbo", "relax", "tile"}
        for name in flag_params:
            if name in midjargon_dict:
                prompt_data[name] = True

    def _process_extra_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process extra parameters."""
        for name, value in midjargon_dict.items():
            if name not in prompt_data and not name.startswith("_"):
                prompt_data["extra_params"][name] = value

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()

        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)

        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)

        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)

        return MidjourneyPrompt(**prompt_data)

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.

        Args:
            midjargon_dict: Dictionary from basic parser or a raw prompt string.

        Returns:
            Validated MidjourneyPrompt.

        Raises:
            ValueError: If the prompt text is empty or if validation fails.
        """
        # Call super() to validate empty prompt
        super().parse_dict(midjargon_dict)

        # Handle version parameters in order of precedence
        if "v" in midjargon_dict:
            value = midjargon_dict["v"]
            if value and str(value) not in VALID_VERSIONS:
                msg = f"Invalid version: {value}"
                raise ValueError(msg)
            midjargon_dict["version"] = f"v{value}"
            del midjargon_dict["v"]
            # Remove niji if present since --v takes precedence
            if "niji" in midjargon_dict:
                del midjargon_dict["niji"]
        elif "niji" in midjargon_dict:
            value = midjargon_dict["niji"]
            if value and str(value) not in VALID_NIJI_VERSIONS:
                msg = f"Invalid niji version: {value}"
                raise ValueError(msg)
            midjargon_dict["version"] = f"niji {value}" if value else "niji"
            del midjargon_dict["niji"]

        # Parse the dictionary
        prompt = self._parse_dict(midjargon_dict)

        # Ensure version precedence
        if "v" in midjargon_dict:
            prompt.version = f"v{midjargon_dict['v']}"
        elif "niji" in midjargon_dict:
            prompt.version = (
                f"niji {midjargon_dict['niji']}" if midjargon_dict["niji"] else "niji"
            )

        return prompt

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
        """Format style parameters for output."""
        params = {}
        if prompt.style:
            params["style"] = prompt.style
        if prompt.version:
            # Convert value to string if it's a list
            version = (
                prompt.version[0]
                if isinstance(prompt.version, list)
                else prompt.version
            )
            if version.lower().startswith("niji"):
                params["niji"] = version[5:] if len(version) > 4 else ""
            else:
                params["v"] = version[1:]
        return params

    def _format_reference_params(
        self, prompt: MidjourneyPrompt
    ) -> dict[str, list[str]]:
        """Format reference parameters for output."""
        params = {}
        if prompt.character_reference:
            params["cref"] = [
                ref[0] if isinstance(ref, list) else ref
                for ref in prompt.character_reference
            ]
        if prompt.style_reference:
            params["sref"] = [
                ref[0] if isinstance(ref, list) else ref
                for ref in prompt.style_reference
            ]
        return params

    def _format_flag_params(self, prompt: MidjourneyPrompt) -> dict[str, None]:
        """Format flag parameters for output."""
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
            return {"aspect": f"{width}:{height}"}
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
        text_value = data.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)
        text = str(text_value).strip()
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
        for name, _default in int_params.items():
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
        for name, _default in float_params.items():
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

        # Updated logic: if '--v' (version) is provided, it takes precedence over '--niji'
        if data.get("version"):
            version_value = data["version"]
            final_version = f"v{version_value}"  # version from --v
        elif data.get("niji"):
            niji_value = data["niji"]
            final_version = f"niji {niji_value}"
        else:
            final_version = None

        # Create prompt object with explicit parameter groups
        prompt_model = MidjourneyPrompt(
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
            version=final_version,
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

        return prompt_model
