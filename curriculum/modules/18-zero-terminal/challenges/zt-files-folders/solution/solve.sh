#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
set -euo pipefail
mkdir radio
mkdir radio/notes
cd radio/notes
pwd > here.txt
cd ../..
ls maze > maze-list.txt
ls maze/north/door-3/blue
echo key-dxjakp > key.txt
