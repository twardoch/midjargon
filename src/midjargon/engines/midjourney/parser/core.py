"""
Core parser implementation for Midjourney engine.
"""

import ast
from typing import Any

from midjargon.core.type_defs import MidjargonDict
from midjargon.engines.base import EngineParser
from midjargon.engines.midjourney.models import ImagePrompt, MidjourneyPrompt
from midjargon.engines.midjourney.parser.exceptions import ParameterValidationError
from midjargon.engines.midjourney.parser.parameters import ParameterHandler


class MidjourneyParser(EngineParser[MidjourneyPrompt]):
    """Parser for Midjourney prompts."""

    def __init__(self) -> None:
        """Initialize parser."""
        self.param_handler = ParameterHandler()

    def _init_prompt_data(self) -> dict[str, Any]:
        """Initialize prompt data with default values."""
        return {
            "text": "",
            "image_prompts": [],
            "stylize": 100,
            "chaos": 0,
            "weird": 0,
            "image_weight": 1.0,
            "seed": None,
            "stop": 100,
            "aspect_width": 1,
            "aspect_height": 1,
            "style": None,
            "version": None,
            "personalization": False,
            "quality": 1.0,
            "character_reference": [],
            "character_weight": 100,
            "style_reference": [],
            "style_weight": None,
            "style_version": 2,
            "repeat": None,
            "turbo": False,
            "relax": False,
            "tile": False,
            "negative_prompt": None,
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
        text = text.strip()
        if not text:
            msg = "Empty prompt"
            raise ValueError(msg)
        prompt_data["text"] = text

        # Process images
        images = midjargon_dict.get("images", [])
        if images:
            prompt_data["image_prompts"] = [ImagePrompt(url=url) for url in images]

    def _process_aspect_ratio(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process aspect ratio parameters."""
        # Check both 'ar' and 'aspect' parameters
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
        except (ValueError, AttributeError) as e:
            msg = f"Invalid aspect ratio format: {value} - must be width:height"
            raise ValueError(msg) from e

        if width <= 0 or height <= 0:
            msg = f"Invalid aspect ratio: {value} - values must be positive"
            raise ValueError(msg)

        prompt_data["aspect_width"] = width
        prompt_data["aspect_height"] = height

    def _process_version(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process version parameter."""
        # Check version parameters in order of precedence
        for name in ("version", "v", "niji"):
            if name not in midjargon_dict:
                continue

            value = midjargon_dict[name]
            if value is None and name == "niji":
                prompt_data["version"] = "niji"
                return

            if value is None:
                continue

            processed_value = self.param_handler.process(name, value)
            if processed_value is not None:
                # Add appropriate prefix
                if name == "niji":
                    prompt_data["version"] = f"niji {processed_value}"
                else:
                    prompt_data["version"] = f"v{processed_value}"
                return

    def _process_style(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process style parameter."""
        if "style" in midjargon_dict:
            value = midjargon_dict["style"]
            if value is not None:
                if isinstance(value, list):
                    value = value[0] if value else None
                if value is not None:
                    prompt_data["style"] = str(value)

    def _process_personalization(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Handle personalization parameter."""
        # Check for both 'p' and 'personalization' keys
        p_value = midjargon_dict.get("p")
        personalization = midjargon_dict.get("personalization")

        # If both are present, personalization takes precedence
        value = personalization if personalization is not None else p_value

        # Handle if value is a string that represents a list
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            try:
                evaluated = ast.literal_eval(value)
                if isinstance(evaluated, list):
                    value = evaluated
            except Exception:
                pass

        # Handle flag-only case (when key exists but value is None or empty string)
        if value is None or value == "":
            prompt_data["personalization"] = True
            return

        # Handle list value
        if isinstance(value, list):
            prompt_data["personalization"] = value if value else False
            return

        # Handle string value - convert to list
        if isinstance(value, str):
            prompt_data["personalization"] = [value]
            return

        # Default case
        prompt_data["personalization"] = False

    def _process_references(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process reference parameters."""
        ref_map = {
            "character_reference": ["character_reference", "cref"],
            "style_reference": ["style_reference", "sref"],
        }

        for target, sources in ref_map.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    if value:
                        prompt_data[target] = (
                            value if isinstance(value, list) else [value]
                        )
                    break

    def _process_numeric_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process numeric parameters."""
        numeric_params = {
            "stylize": ["s", "stylize"],
            "chaos": ["c", "chaos"],
            "weird": ["w", "weird"],
            "image_weight": ["iw", "image_weight"],
            "seed": ["seed"],
            "stop": ["stop"],
            "quality": ["q", "quality"],
            "character_weight": ["cw", "character_weight"],
            "style_weight": ["sw", "style_weight"],
            "style_version": ["sv", "style_version"],
            "repeat": ["r", "repeat"],
        }

        for target, sources in numeric_params.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    try:
                        processed = self.param_handler.process(source, value)
                        if value is None:  # Explicitly set None values
                            prompt_data[target] = None
                        elif processed is not None:
                            prompt_data[target] = processed
                        break
                    except ParameterValidationError as e:
                        raise ValueError(str(e)) from e

    def _process_flag_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process flag parameters."""
        flag_params = {
            "turbo": ["turbo"],
            "relax": ["relax"],
            "tile": ["tile"],
        }

        for target, sources in flag_params.items():
            for source in sources:
                if source in midjargon_dict:
                    value = midjargon_dict[source]
                    try:
                        processed = self.param_handler.process(source, value)
                        if processed is not None:
                            prompt_data[target] = processed
                            break
                        if value is None:  # Handle flag parameters without values
                            prompt_data[target] = True
                            break
                    except ParameterValidationError as e:
                        raise ValueError(str(e)) from e

        # Handle personalization separately
        for source in ["p", "personalization"]:
            if source in midjargon_dict:
                value = midjargon_dict[source]
                if value is None or value == "":
                    prompt_data["personalization"] = True
                else:
                    prompt_data["personalization"] = [value]
                break

    def _process_negative_prompt(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process negative prompt parameter."""
        if "no" in midjargon_dict:
            value = midjargon_dict["no"]
            if isinstance(value, str):
                prompt_data["negative_prompt"] = value

    def _process_extra_params(
        self, prompt_data: dict[str, Any], midjargon_dict: MidjargonDict
    ) -> None:
        """Process extra parameters."""
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
            if (
                name not in excluded_fields
                and not name.startswith("_")
                and (
                    value is None or isinstance(value, str | int | float | bool | list)
                )
            ):
                prompt_data["extra_params"][name] = (
                    str(value) if not isinstance(value, list | type(None)) else value
                )

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt object.

        Args:
            midjargon_dict: Dictionary to parse.

        Returns:
            MidjourneyPrompt object.

        Raises:
            ValueError: If data is invalid.
        """
        prompt_data = self._init_prompt_data()

        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)

        # Process parameters in order
        self._process_version(prompt_data, midjargon_dict)
        self._process_style(prompt_data, midjargon_dict)
        self._process_personalization(prompt_data, midjargon_dict)
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_references(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_negative_prompt(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)

        return MidjourneyPrompt(**prompt_data)

    def _format_numeric_params(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format numeric parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of formatted numeric parameters.
        """
        numeric_params = {
            "stylize": "s",
            "chaos": "c",
            "weird": "w",
            "image_weight": "iw",
            "seed": "seed",
            "stop": "stop",
            "quality": "q",
            "character_weight": "cw",
            "style_weight": "sw",
            "style_version": "sv",
            "repeat": "r",
        }

        result = {}
        for attr, param_name in numeric_params.items():
            value = getattr(prompt, attr)
            if value is not None:
                result[param_name] = str(value)
        return result

    def _format_version(self, version: str | None) -> dict[str, str]:
        """Format version parameter for dictionary output.

        Args:
            version: Version string.

        Returns:
            Dictionary with formatted version parameter.
        """
        if not version:
            return {}

        if version.lower().startswith("niji"):
            parts = version.split()
            return {"niji": parts[1] if len(parts) > 1 else ""}

        version_value = version[1:] if version.startswith("v") else version
        return {"v": version_value}

    def _format_flags(self, prompt: MidjourneyPrompt) -> dict[str, None]:
        """Format flag parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of flag parameters.
        """
        result = {}
        for flag in ("turbo", "relax", "tile"):
            if getattr(prompt, flag):
                result[flag] = None
        return result

    def _format_references(self, prompt: MidjourneyPrompt) -> dict[str, str]:
        """Format reference parameters for dictionary output.

        Args:
            prompt: MidjourneyPrompt instance.

        Returns:
            Dictionary of reference parameters.
        """
        result = {}
        if prompt.character_reference:
            result["cref"] = prompt.character_reference
        if prompt.style_reference:
            result["sref"] = prompt.style_reference
        return result

    def _format_aspect_ratio(self, width: int, height: int) -> dict[str, str]:
        """Format aspect ratio for dictionary output.

        Args:
            width: Aspect ratio width.
            height: Aspect ratio height.

        Returns:
            Dictionary with aspect ratio if non-default.
        """
        if width != 1 or height != 1:
            return {"aspect": f"{width}:{height}"}
        return {}

    def to_dict(self, prompt: MidjourneyPrompt) -> dict[str, Any]:
        """Convert a MidjourneyPrompt back to a dictionary.

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

        # Add style
        if prompt.style:
            result["style"] = prompt.style

        # Add version
        result.update(self._format_version(prompt.version))

        # Add references
        result.update(self._format_references(prompt))

        # Add flags
        result.update(self._format_flags(prompt))

        # Add negative prompt
        if prompt.negative_prompt is not None:
            result["no"] = prompt.negative_prompt

        # Add extra parameters
        result.update(prompt.extra_params)

        return result

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt object.

        This is the implementation of the abstract method from EngineParser.

        Args:
            midjargon_dict: Dictionary to parse.

        Returns:
            MidjourneyPrompt object.

        Raises:
            ValueError: If data is invalid.
        """
        return self.parse_dict(midjargon_dict)
