"""
midjargon.engines.base
~~~~~~~~~~~~~~~~~~~

Base engine interface for midjargon.

This module provides the abstract base class that all engine parsers must implement.
Engine parsers are responsible for converting between the generic MidjargonDict format
and engine-specific prompt types.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from midjargon.core.type_defs import MidjargonDict

# Type variable for engine-specific prompt type, must be a Pydantic model
T = TypeVar("T", bound=BaseModel)


class EngineParser(ABC, Generic[T]):
    """
    Base class for engine-specific parsers.

    Each engine parser is responsible for:
    1. Converting MidjargonDict to engine-specific prompt types
    2. Validating parameters according to engine rules
    3. Converting engine-specific prompts back to dictionaries

    Type Parameters:
        T: The engine-specific prompt type (must be a Pydantic model)
    """

    @abstractmethod
    def parse_dict(self, midjargon_dict: MidjargonDict) -> T:
        """
        Parse a MidjargonDict into an engine-specific prompt type.

        This method should:
        1. Extract relevant fields from the input dictionary
        2. Convert parameter values to appropriate types
        3. Validate all values according to engine rules
        4. Construct and return a validated prompt object

        Args:
            midjargon_dict: Dictionary from basic parser containing:
                - "text": The main prompt text
                - "images": List of image URLs (if any)
                - "parameters": Dictionary of parameter name/value pairs

        Returns:
            An engine-specific prompt object.

        Raises:
            ValueError: If the input dictionary is invalid for this engine.
        """
        if not midjargon_dict.get("text") and not midjargon_dict.get("images"):
            msg = "Empty prompt: must provide text or image URLs"
            raise ValueError(msg)

    @abstractmethod
    def to_dict(self, prompt: T) -> dict[str, Any]:
        """
        Convert an engine-specific prompt back to a dictionary.

        This method should:
        1. Extract all relevant fields from the prompt
        2. Convert values to appropriate string representations
        3. Structure the output to match MidjargonDict format

        Args:
            prompt: Engine-specific prompt instance.

        Returns:
            Dictionary with keys:
                - "text": The main prompt text
                - "images": List of image URLs (if any)
                - Additional parameter key/value pairs
        """
        pass

    def validate(self, prompt: T) -> bool:
        """
        Validate an engine-specific prompt.

        By default, this uses Pydantic validation. Override this method
        to implement additional engine-specific validation rules.

        Args:
            prompt: Engine-specific prompt to validate.

        Returns:
            True if the prompt is valid, False otherwise.

        Raises:
            ValueError: If validation fails with specific error messages.
        """
        # Basic Pydantic validation
        prompt.model_validate(prompt.model_dump())
        return True
