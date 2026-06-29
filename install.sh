#!/usr/bin/env bash
# install.sh: Install midjargon in editable mode
# midjargon: Parse and manipulate Midjourney-style prompts

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installing midjargon (editable) ==="
uv pip install -e .
echo "=== Install complete ==="
