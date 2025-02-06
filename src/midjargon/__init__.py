"""Package initialization functionality."""

from importlib import metadata

from .midjargon import MidjargonPrompt, parse_prompt

__version__ = metadata.version(__name__)
__all__ = ["MidjargonPrompt", "__version__", "parse_prompt"]
