#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///

"""
Main entry point for midjargon CLI.
"""

import fire

from .cli import main

if __name__ == "__main__":
    fire.Fire(main)
