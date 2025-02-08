#!/bin/env bash
# this_file: test-cases/prompts.sh

# THIS READS PROMPTS FROM prompts-in.txt
# THE ERRORS are in prompts-out.txt
# THE OUTPUT OF THE midjargon commands are in the -mj -fal -json -perm files

cat ./prompts-in.txt | while read p; do
    for o in mj fal json perm; do
        echo "> $o '$p'"
        echo "======" >>prompts-$o.txt
        echo $p >>prompts-$o.txt
        python -m midjargon $o "$p" -j >>prompts-$o.txt
    done

done
