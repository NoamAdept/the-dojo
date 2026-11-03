#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# Prints the flag on its last line.
set -euo pipefail
printf '%s\n' 'printenv | grep "^LAB_"' 'printf "%s\n" "${LAB_FLAG_PART1}${LAB_FLAG_PART2}"' | ./lab_shell.sh
