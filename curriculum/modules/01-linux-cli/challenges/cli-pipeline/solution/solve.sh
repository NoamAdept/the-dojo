#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
set -euo pipefail
grep ',north,' readings.csv | sort -t, -k3,3nr | head -n 3 | cut -d, -f1 > answer.txt
