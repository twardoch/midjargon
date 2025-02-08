#!/usr/bin/env bash
# this_file: midjargon/printme.sh
if [ -e ./midjargon.txt ]; then
    rm ./midjargon.txt
fi
if [ -z "$VIRTUAL_ENV" ]; then
    uv pip install --system gitignore-find
else
    uv pip install gitignore-find
fi
printfolder . ../midjargon.txt && mv ../midjargon.txt .
