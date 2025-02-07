#!/usr/bin/env -S uv run
# /// script
# dependencies = ["fire", "rich", "pydantic"]
# ///

"""
Main entry point for midjargon CLI.
"""


from midjargon.cli.main import main

if __name__ == "__main__":
    main()
