#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# data/settings.txt and config.txt are typed in vim; they sit next to this script.
set -euo pipefail
./greet > greet.txt
chmod +x locked
./locked > locked.txt
./report > report.txt
./checkme
