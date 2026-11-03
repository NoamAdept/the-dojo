#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
set -euo pipefail
echo Hello terminal > hello.txt
whoami > me.txt
date > today.txt
echo first > list.txt
echo second >> list.txt
