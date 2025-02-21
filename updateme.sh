#!/usr/bin/env bash
# this_file: ./printme.sh
uv venv
# Activate venv if not active
if [[ -z "${VIRTUAL_ENV}" ]] && [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
    uv pip install fire gitignore-find
fi
uv pip install -e .[all]
if [ -e ./midjargon.txt ]; then
    rm ./midjargon.txt
fi
if [ -z "$VIRTUAL_ENV" ]; then
    uv pip install --system gitignore-find
else
    uv pip install gitignore-find
fi
printfolder . ../midjargon.txt && mv ../midjargon.txt .

hatch run lint:style >ERRORS.txt
hatch test >>ERRORS.txt

cat midjargon.txt ERRORS.txt

echo ">> The codebase is in @midjargon.txt and the recent errors are in @ERRORS.txt"
