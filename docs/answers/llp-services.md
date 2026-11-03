## Services, Ports and Logs

*llp-services · easy*

**Goal.** Fill in `answers/task1.sh` to `answers/task5.sh` to start a small web server in the background, query a server with curl, find which port is listening, read a port from a log, and change a config then restart a service.

**You need to know.**

- `python3 -m http.server PORT --bind 127.0.0.1` serves the current folder.
- `&` backgrounds a command, `$!` is the PID of the last background job, `> file 2>&1` sends both output streams to a file.
- `curl -s URL` fetches quietly; its exit code is 0 only when it connected.
- `grep | tail -n 1` gets the last match; `sed -i "s/^key=.*/key=value/"` edits one line in place.
- A service reads its config at start, so a config change needs a restart.

**Walkthrough.**

`./check` picks new random high ports each run and stops every server afterwards, so never hard-code a port. Remove the `# TODO` line from every file.

1. Task 1, start a server in the background.

   ```bash
   #!/bin/bash
   python3 -m http.server "$(cat port.txt)" --bind 127.0.0.1 > server.log 2>&1 &
   echo $! > server.pid
   ```

   The `&` lets the script finish while the server keeps running, `2>&1` catches the server's messages (it logs to stderr), and `$!` saves its PID.

2. Task 2, ask the server for `/status.txt`.

   ```bash
   #!/bin/bash
   curl -s "http://127.0.0.1:$(cat port.txt)/status.txt"
   ```

   The port goes into the URL after a colon; `-s` hides the progress bar so only the file content prints.

3. Task 3, which port in `ports.txt` is listening.

   ```bash
   #!/bin/bash
   for p in $(cat ports.txt); do
       if curl -s -o /dev/null "http://127.0.0.1:$p/"; then
           echo "$p"
       fi
   done
   ```

   `curl` fails with "connection refused" on a closed port, so only the open one passes the `if`; `-o /dev/null` throws away the page itself.

4. Task 4, port from the last `listening on` line.

   ```bash
   #!/bin/bash
   grep 'listening on' service.log | tail -n 1 | awk -F: '{print $NF}'
   ```

   The lines end in `127.0.0.1:PORT`; splitting on `:` and printing the last field (`$NF`) gives the port even though the timestamp has colons too.

5. Task 5, edit the config and restart.

   ```bash
   #!/bin/bash
   sed -i "s/^port=.*/port=$(cat new_port.txt)/" beacon.conf
   ./ctl.sh restart
   ```

   The `^port=` anchor changes only that one line, and `restart` stops the old process before starting a new one that reads the new port.

6. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Forgetting the `&` in task 1: the script never finishes and the checker times out.
- Editing `beacon.conf` but not restarting, or starting a second copy without stopping the old one; the checker wants the old port closed.
- Using `head` instead of `tail` in task 4; the log has several starts and only the last one counts.
