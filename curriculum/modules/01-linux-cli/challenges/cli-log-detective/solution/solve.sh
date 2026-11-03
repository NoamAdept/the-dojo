#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
set -euo pipefail
grep ' level=WARN ' receiver.log | cut -d' ' -f3 | cut -d= -f2 | sort | uniq -c | awk '{print $2 "=" $1}' > report.txt
