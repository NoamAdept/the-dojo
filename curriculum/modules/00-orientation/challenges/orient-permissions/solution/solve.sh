#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# Prints the flag on its last line.
set -euo pipefail
ls -l vault
chmod u+r vault/flag.txt
cat vault/flag.txt
