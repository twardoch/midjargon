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
                "iw": (
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
                "cw": (
                    float,
                    lambda x: self._validate_numeric_range("character_weight", x),
                ),
                "style_weight": (
                    float,
                    lambda x: self._validate_numeric_range("style_weight", x),
                ),
                "sw": (
                    float,
                    lambda x: self._validate_numeric_range("style_weight", x),
                ),
                "style_version": (
                    int,
                    lambda x: self._validate_numeric_range("style_version", x),
                ),
                "sv": (
                    int,
                    lambda x: self._validate_numeric_range("style_version", x),
                ),
                "repeat": (int, lambda x: self._validate_numeric_range("repeat", x)),
            }

            if name in param_types:
                type_func, validate_func = param_types[name]
                val = type_func(
                    float(str(value))
                )  # Convert through float for int/float compatibility
                validate_func(val)
                # Map shorthand names to full names
                name_map = {
                    "iw": "image_weight",
                    "cw": "character_weight",
                    "sw": "style_weight",
                    "sv": "style_version",
                }
                return name_map.get(name, name), val

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

    def _validate_niji_version(self, version: str) -> bool:
        """Validate niji version number."""
        parts = version.split()
        if len(parts) > 1:
            version_num = parts[1]
            return version_num in VALID_NIJI_VERSIONS
        return True  # Just "niji" is valid

    def _validate_standard_version(self, version: str) -> bool:
        """Validate standard version number."""
        version_num = version[1:] if version.startswith("v") else version
        return version_num in VALID_VERSIONS

    def _normalize_version_value(self, value: str | list[str] | None) -> str | None:
        """Normalize version value to string."""
        if isinstance(value, list):
            value = value[0] if value else None
        return str(value) if value is not None else None

    def _validate_niji_version_parts(self, parts: list[str]) -> None:
        """Validate niji version parts."""
        if len(parts) > 1 and parts[1] not in VALID_NIJI_VERSIONS:
            msg = f"Invalid niji version: {parts[1]}"
            raise ValueError(msg)

    def _handle_niji_specific(self, new_value: str | None) -> tuple[str, str]:
        """Handle niji-specific version parameter."""
        if new_value and str(new_value) not in VALID_NIJI_VERSIONS:
            msg = f"Invalid niji version: {new_value}"
            raise ValueError(msg)
        return "version", f"niji {new_value}" if new_value else "niji"

    def _handle_standard_version(self, new_value: str) -> tuple[str, str]:
        """Handle standard version parameter."""
        version_str = str(new_value)
        if version_str.startswith("v"):
            version_str = version_str[1:]
        if not version_str or version_str not in VALID_VERSIONS:
            msg = f"Invalid version: {new_value}"
            raise ValueError(msg)
        return "version", f"v{version_str}"

    def _handle_version_param(
        self, name: str, raw_value: str | list[str] | None
    ) -> tuple[str | None, Any]:
        """Handle version parameter conversion."""
        value = self._normalize_version_value(raw_value)
        if value is None:
            if name == "niji":
                return "version", "niji"
            return None, None

        new_value = value[0] if isinstance(value, list) and value else value

        # Handle niji version format
        if isinstance(new_value, str) and new_value.lower().startswith("niji"):
            parts = new_value.split()
            self._validate_niji_version_parts(parts)
            return "version", new_value

        if name == "niji":
            return self._handle_niji_specific(new_value)

        if name in ("v", "version"):
            return self._handle_standard_version(new_value)

        return None, None

    def _handle_personalization(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Handle personalization parameter."""
        if "p" in midjargon_dict or "personalization" in midjargon_dict:
            raw_value = midjargon_dict.get("p") or midjargon_dict.get("personalization")
            if raw_value is not None:
                processed_value = (
                    raw_value[0]
                    if isinstance(raw_value, list) and raw_value
                    else raw_value
                )
                if processed_value is not None:
                    prompt_data["personalization"] = str(processed_value)

    def _convert_numeric_param(self, param_name: str, value: Any) -> int | float:
        """Convert parameter value to appropriate numeric type."""
        if param_name in {
            "stylize",
            "chaos",
            "weird",
            "seed",
            "stop",
            "repeat",
            "style_version",
        }:
            return int(float(str(value)))
        return float(str(value))

    def _process_numeric_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process numeric parameters."""
        numeric_params = {
            "s": "stylize",
            "stylize": "stylize",
            "c": "chaos",
            "chaos": "chaos",
            "w": "weird",
            "weird": "weird",
            "iw": "image_weight",
            "image_weight": "image_weight",
            "seed": "seed",
            "stop": "stop",
            "q": "quality",
            "quality": "quality",
            "cw": "character_weight",
            "character_weight": "character_weight",
            "sw": "style_weight",
            "style_weight": "style_weight",
            "sv": "style_version",
            "style_version": "style_version",
            "r": "repeat",
            "repeat": "repeat",
        }
        self._handle_personalization(prompt_data, midjargon_dict)

        for name, raw_value in midjargon_dict.items():
            if name not in numeric_params:
                continue

            try:
                if raw_value is None:
                    continue

                processed_value = (
                    raw_value[0]
                    if isinstance(raw_value, list) and raw_value
                    else raw_value
                )
                if processed_value is None:
                    continue

                param_name = numeric_params[name]
                param_value = self._convert_numeric_param(param_name, processed_value)
                self._validate_numeric_range(param_name, param_value)
                prompt_data[param_name] = param_value

            except (ValueError, TypeError) as e:
                msg = f"Invalid numeric value for {name}: {raw_value}"
                raise ValueError(msg) from e

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
        if "ar" in midjargon_dict or "aspect" in midjargon_dict:
            value = midjargon_dict.get("ar") or midjargon_dict.get("aspect")

            if value is None:
                return

            if isinstance(value, list):
                value = value[0] if value else None
                if value is None:
                    return

            try:
                width_str, height_str = str(value).split(":")
                width = int(width_str)
                height = int(height_str)

                if width <= 0 or height <= 0:
                    msg = f"Invalid aspect ratio: {value} - values must be positive"
                    raise ValueError(msg)

                prompt_data["aspect_width"] = width
                prompt_data["aspect_height"] = height

            except (ValueError, AttributeError) as e:
                msg = f"Invalid aspect ratio format: {value} - must be width:height"
                raise ValueError(msg) from e

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
        # List of fields that should not be included in extra_params
        excluded_fields = {
            "text",
            "images",
            "aspect",
            "ar",
            "style",
            "version",
            "v",
            "niji",
            "stylize",
            "s",
            "chaos",
            "c",
            "weird",
            "w",
            "image_weight",
            "iw",
            "seed",
            "stop",
            "quality",
            "q",
            "character_weight",
            "cw",
            "style_weight",
            "sw",
            "style_version",
            "sv",
            "repeat",
            "r",
            "turbo",
            "relax",
            "tile",
            "negative_prompt",
            "no",
            "character_reference",
            "cref",
            "style_reference",
            "sref",
            "personalization",
            "p",
        }

        for name, value in midjargon_dict.items():
            if name not in excluded_fields and not name.startswith("_"):
                if value is None or isinstance(value, str | int | float | bool | list):
                    prompt_data["extra_params"][name] = (
                        str(value)
                        if not isinstance(value, list | type(None))
                        else value
                    )

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

    def _validate_text(self, data: MidjargonDict) -> str:
        """Validate and extract text from data."""
        text_value = data.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)
        text = str(text_value).strip()
        if not text:
            msg = "Empty prompt text"
            raise ValueError(msg)
        return text

    def _process_images(self, data: MidjargonDict) -> list[ImagePrompt]:
        """Process and validate image prompts."""
        image_prompts = []
        images = data.get("images", [])
        if images is not None:
            for image_url in images:
                if not isinstance(image_url, str):
                    msg = f"Invalid image URL: {image_url}"
                    raise ValueError(msg)
                image_prompts.append(ImagePrompt(url=image_url))
        return image_prompts

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

    def _get_numeric_param_mapping(self) -> dict[str, str]:
        """Get mapping of prompt attributes to parameter names."""
        return {
            "stylize": "stylize",
            "chaos": "chaos",
            "weird": "weird",
            "image_weight": "iw",
            "seed": "seed",
            "stop": "stop",
            "quality": "quality",
            "repeat": "repeat",
            "character_weight": "cw",
            "style_weight": "sw",
            "style_version": "sv",
        }

    def _add_numeric_param(
        self, params: dict[str, str], _: str, value: Any, param_name: str
    ) -> None:
        """Add a numeric parameter to the params dictionary if it exists."""
        if value is not None:
            params[param_name] = str(value)

    def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format numeric parameters for dictionary output."""
        params = {}
        param_mapping = self._get_numeric_param_mapping()

        for attr, param_name in param_mapping.items():
            self._add_numeric_param(params, attr, getattr(prompt, attr), param_name)

        return params

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
        prompt_data = self._get_default_prompt_data()

        # Process text and images
        prompt_data["text"] = self._validate_text(data)
        prompt_data["image_prompts"] = self._process_images(data)

        # Process parameters
        self._process_numeric_params(prompt_data, data)
        self._process_aspect_ratio(data, prompt_data)
        self._process_version(data, prompt_data)

        # Process style and reference parameters
        self._process_style_params(prompt_data, data)
        self._process_reference_params(prompt_data, data)

        # Process flag parameters
        self._process_flag_params(prompt_data, data)

        # Process extra parameters
        self._process_extra_params(prompt_data, data)

        return MidjourneyPrompt(**prompt_data)

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
                    raise ValueError(msg) from None

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
        """Process text and image components of the prompt."""
        # Process text
        text = midjargon_dict.get("text", "")
        if text is None:
            text = ""
        if isinstance(text, list):
            text = text[0] if text else ""
        prompt_data["text"] = text.strip()

        # Process images
        images = midjargon_dict.get("images", [])
        if images:
            prompt_data["image_prompts"] = [ImagePrompt(url=url) for url in images]

    def _process_version(
        self, data: MidjargonDict, prompt_data: dict[str, Any]
    ) -> None:
        """Process version parameter."""
        if "version" in data:
            version = str(data["version"])
            if version.startswith("niji"):
                parts = version.split()
                if len(parts) > 1 and parts[1] not in VALID_NIJI_VERSIONS:
                    msg = f"Invalid niji version: {parts[1]}"
                    raise ValueError(msg) from None
            else:
                version_num = version[1:] if version.startswith("v") else version
                if version_num not in VALID_VERSIONS:
                    msg = f"Invalid version: {version_num}"
                    raise ValueError(msg) from None
            prompt_data["version"] = version
