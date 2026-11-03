# Services, Ports and Logs

**What you will learn:**

- what a service is,
- what localhost and ports are,
- how to start, test, read and restart a small service from the shell.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`.
`./check` runs each script in a new, empty folder.
It picks new random high port numbers each time.
When it is done, it stops every server that it or you started.

1. **Start a server**: start `python3 -m http.server` in the background. Use the port in `port.txt`. Bind it to `127.0.0.1`, and let it share the current folder. Send its output to `server.log`. Write its PID to `server.pid`. Your script must finish. (The server keeps running after your script ends.)
2. **Ask it something**: a server is already running on the port in `port.txt`. Use curl to print the contents of its file `/status.txt`.
3. **Which port?**: `ports.txt` lists a few port numbers, 1 on each line. A server is listening on exactly 1 of them. Print that port number.
4. **Read the log**: `service.log` is the log of a service. The service started several times. Print the port number from the **last** line that contains `listening on`.
5. **Edit and restart**: a service is running with the settings in `beacon.conf`. You control it with `./ctl.sh` (`start`, `stop`, `restart`). Change only the `port=` line, to the number in `new_port.txt`. Then restart the service. It must listen on the new port, and not on the old one any more.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
