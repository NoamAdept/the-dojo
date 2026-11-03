#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
set -euo pipefail
grep -Eo '[0-9]+\.[0-9]+ MHz' bulletin.txt | cut -d' ' -f1 | sort -n -u > frequencies.txt
