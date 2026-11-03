## System Investigation

*orient-system-investigation · hard*

**Goal.** EchoRelay, a local TCP service, has three stacked faults: a wrong token path, an unreadable token file, and a port that does not match the contract. Fix them until `./echorelay/verify.sh` prints a flag.

**You need to know.**

- Triage one subsystem at a time: process, config, permissions, network (README, "Steps").
- `diff` to compare config with the example, `ls -l` and `chmod u+r` for file modes.
- `verify.sh` is the contract: it sends `PING` to `127.0.0.1:9471`. Do not edit it.
- `relayctl.sh start|stop|status|logs` controls the worker.

**Walkthrough.**

1. Try it and read the contract.

   ```bash
   ./echorelay/relayctl.sh start
   ./echorelay/verify.sh
   cat echorelay/verify.sh
   ```

   The start fails, verify prints an empty `response:`, and the script shows it always talks to port `9471`.

2. Read the log.

   ```bash
   ./echorelay/relayctl.sh logs
   ```

   It says `ERROR: cannot read dropbox .../echorelay/dropbox/token.missing.txt: No such file or directory`.

3. Compare the config with the example.

   ```bash
   diff echorelay/config/relay.conf echorelay/config/relay.conf.example
   ```

   Two lines differ: `listen_port=9470` (contract says `9471`) and `dropbox_path=echorelay/dropbox/token.missing.txt` (real file is `token.txt`).

4. Fix both config lines.

   ```bash
   sed -i 's/^listen_port=.*/listen_port=9471/' echorelay/config/relay.conf
   sed -i 's#^dropbox_path=.*#dropbox_path=echorelay/dropbox/token.txt#' echorelay/config/relay.conf
   ```

   The port must match what `verify.sh` dials, and the worker needs the path of a file that exists.

5. Start again and find the permission fault.

   ```bash
   ./echorelay/relayctl.sh start
   ls -l echorelay/dropbox
   ```

   The error is now `Permission denied` on `token.txt`, and `ls -l` shows `----------`.

6. Give the owner read permission.

   ```bash
   chmod u+r echorelay/dropbox/token.txt
   ```

   The worker runs as you, so owner read is enough.

7. Start, confirm it stays up, and verify.

   ```bash
   ./echorelay/relayctl.sh start
   ./echorelay/relayctl.sh status
   ./echorelay/verify.sh
   ```

   `status` says `running pid NNNN`, and verify prints `response: PONG flag{...}`, then `VERIFY OK`, then the flag on its own line.

8. Submit and stop the worker.

   ```bash
   academy submit 'flag{...}'
   ./echorelay/relayctl.sh stop
   ```

**Check.** `./echorelay/verify.sh` prints `VERIFY OK` followed by the flag.

**Common mistakes.**

- Editing `verify.sh` to use port 9470. The task forbids it, and the fix belongs in `relay.conf`.
- Stopping and restarting after a good start: the session secret is consumed on the first successful start, so the worker exits with `RELAY_SESSION_FLAG missing`. Press Start in the dojo again.
- Testing as root: root reads a mode `000` file anyway, so the permission fault never shows. Test as a normal user.
