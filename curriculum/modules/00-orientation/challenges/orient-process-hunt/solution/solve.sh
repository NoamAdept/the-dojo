#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# ./check then compares report.txt with the live helper process.
set -euo pipefail
./run
sleep 1
# On a shared server other learners run helpers too: take the one started in this folder.
pid=""
for p in $(pgrep -f 'helper --work'); do
  [ "$(readlink /proc/$p/cwd 2>/dev/null)" = "$(pwd -P)" ] && pid=$p
done
cmd=$(tr '\0' ' ' < /proc/$pid/cmdline | sed 's/ $//')
notes=${cmd##*--notes }
code=$(sed -n 's/^secret_code=//p' "$notes")
cat > report.txt <<REPORT
process_number=$pid
full_command=$cmd
folder=$(readlink /proc/$pid/cwd)
notes_file=$notes
secret_code=$code
REPORT
cat report.txt
