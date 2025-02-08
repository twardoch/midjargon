#!/usr/bin/env python3
# this_file: src/midjargon/engines/midjourney/__init__.py

from midjargon.engines.midjourney.midjourney import MidjourneyParser


class MidjourneyPrompt:
    """Stub class for Midjourney prompt."""

    def __init__(self, prompt: str = ""):
        self.prompt = prompt


def parse_midjourney_dict(prompt: str) -> dict:
    """Stub function for converting a prompt to a dictionary."""
    return {"prompt": prompt}
