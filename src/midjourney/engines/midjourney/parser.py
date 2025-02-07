from typing import Any


class MidjourneyParser:
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
        if not isinstance(midjargon_dict, dict):
            midjargon_dict = {"text": str(midjargon_dict)}

        # Validate text is not empty
        text_value = midjargon_dict.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)

        if isinstance(text_value, list):
            text = text_value[0] if text_value else ""
        else:
            text = str(text_value)

        if not text.strip():
            msg = "Empty prompt text"
            raise ValueError(msg)

        # ... rest of the existing code follows unchanged
