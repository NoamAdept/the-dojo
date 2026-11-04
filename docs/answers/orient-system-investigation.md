# Autopsy of a Pi

`orient-system-investigation` · Yellow Belt

**Goal:** EchoRelay, a local TCP service, has three stacked faults: a wrong token path, an unreadable token file, and a port that does not match the contract. Fix them until `./echorelay/verify.sh` prints a flag.

Type in the challenge folder. The last line shows the flag:

```bash
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
```

Paste the flag in the flag box and press **Submit**.
