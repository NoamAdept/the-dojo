# The Silent Port

`orient-broken-service` · Yellow Belt

**Goal:** The local "beacon" web service will not start. Read its log, fix the two bad values in `service/config/beacon.conf`, start it, and read the flag from its live `/health` response.

Type in the challenge folder. The last line shows the flag:

```bash
diff service/config/beacon.conf service/config/beacon.conf.example || true
sed -i 's/^listen_host=.*/listen_host=127.0.0.1/' service/config/beacon.conf
sed -i 's#^data_path=.*#data_path=service/data/beacon_ok.json#' service/config/beacon.conf
./service/beaconctl.sh start
sleep 1
health=$(curl -s http://127.0.0.1:8765/health)
./service/beaconctl.sh stop
echo "$health"
echo "$health" | grep -o 'flag{[^}]*}'
```

Paste the flag in the flag box and press **Submit**.
