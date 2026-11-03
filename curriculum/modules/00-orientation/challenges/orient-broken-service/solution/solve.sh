#!/usr/bin/env bash
# Answer used by scripts/verify_answers.py: the walkthrough commands, run in the challenge folder.
# Prints the flag on its last line.
set -euo pipefail
diff service/config/beacon.conf service/config/beacon.conf.example || true
sed -i 's/^listen_host=.*/listen_host=127.0.0.1/' service/config/beacon.conf
sed -i 's#^data_path=.*#data_path=service/data/beacon_ok.json#' service/config/beacon.conf
./service/beaconctl.sh start
sleep 1
health=$(curl -s http://127.0.0.1:8765/health)
./service/beaconctl.sh stop
echo "$health"
echo "$health" | grep -o 'flag{[^}]*}'
