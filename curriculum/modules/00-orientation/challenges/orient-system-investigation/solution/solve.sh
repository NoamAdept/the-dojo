#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# Prints the flag on its last line.
set -euo pipefail
diff echorelay/config/relay.conf echorelay/config/relay.conf.example || true
sed -i 's/^listen_port=.*/listen_port=9471/' echorelay/config/relay.conf
sed -i 's#^dropbox_path=.*#dropbox_path=echorelay/dropbox/token.txt#' echorelay/config/relay.conf
chmod u+r echorelay/dropbox/token.txt
./echorelay/relayctl.sh start
sleep 1
./echorelay/relayctl.sh status
out=$(./echorelay/verify.sh)
./echorelay/relayctl.sh stop
echo "$out"
echo "$out" | grep -o 'flag{[^}]*}' | tail -1
