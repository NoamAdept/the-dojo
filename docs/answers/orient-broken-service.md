## Broken Service

*orient-broken-service · hard*

**Goal.** The local "beacon" web service will not start. Read its log, fix the two bad values in `service/config/beacon.conf`, start it, and read the flag from its live `/health` response.

**You need to know.**

- The debug loop: start, read the log, compare with a known-good config, fix, start again.
- `diff FILE1 FILE2` shows lines that differ.
- `127.0.0.1` is loopback (this machine only); `0.0.0.0` means every network interface.
- `curl -s URL` fetches a web page from the terminal.

**Walkthrough.**

1. Try to start it.

   ```bash
   ./service/beaconctl.sh start
   ```

   It prints `failed to stay up` and the reason: `ERROR: refuse to bind non-loopback host=0.0.0.0`. `./service/beaconctl.sh logs` shows the same line later.

2. Compare the config with the example.

   ```bash
   diff service/config/beacon.conf service/config/beacon.conf.example
   ```

   Two real differences: `listen_host=0.0.0.0` (should be `127.0.0.1`) and `data_path=service/data/missing_beacon.json` (should be `service/data/beacon_ok.json`). The port, `8765`, is already correct.

3. Fix the host. Edit with `vim service/config/beacon.conf` (press `i` to type, `Esc` then `:wq` Enter to save and quit) or:

   ```bash
   sed -i 's/^listen_host=.*/listen_host=127.0.0.1/' service/config/beacon.conf
   ```

   The server refuses any address that is not loopback, so the service stays local.

4. Start again to see the next fault.

   ```bash
   ./service/beaconctl.sh start
   ```

   Now it says `ERROR: data file missing: .../service/data/missing_beacon.json`. That file does not exist; `ls service/data` shows `beacon_ok.json`.

5. Fix the data path and start.

   ```bash
   sed -i 's#^data_path=.*#data_path=service/data/beacon_ok.json#' service/config/beacon.conf
   ./service/beaconctl.sh start
   ```

   This time it prints `started pid NNNN`, and the log says `INFO: listening on 127.0.0.1:8765`.

6. Ask the live service for its health.

   ```bash
   curl -s http://127.0.0.1:8765/health
   ```

   The JSON has a `"flag"` field. The flag is injected by the running process, not stored in `beacon_ok.json`.

7. Submit it, then stop the service.

   ```bash
   academy submit 'flag{...}'
   ./service/beaconctl.sh stop
   ```

**Check.** `curl -s http://127.0.0.1:8765/health` returns JSON with `"status": "ok"` and a `"flag"` field; the dojo accepts that flag.

**Common mistakes.**

- Stopping and restarting after a successful start, then wondering why `"flag"` is gone. The secret file is consumed on the first good start; press Start in the dojo again to get a fresh one.
- Fixing the host to the machine's LAN address or `localhost` with a typo. Use `127.0.0.1` exactly as in the example.
- Looking for the flag in the files on disk; it only exists in the live `/health` response.
