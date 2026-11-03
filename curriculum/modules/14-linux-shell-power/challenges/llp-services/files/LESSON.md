# Services, Ports and Logs: lesson

### Services and daemons

Most programs you have run so far start, do 1 job and then exit (stop).
A **service** is different. On Linux, a service is often called a **daemon**.
It is a program that keeps running in the background.
It waits for other programs to ask it for something.
A web server is a service: it waits for requests and answers each one.

### Addresses and ports

Other programs must be able to reach a service.
So a service **listens** (waits for connections) on an address and a port.

- The **address** says which computer.
  `127.0.0.1` is also called **localhost** or **loopback**.
  It means "this computer only". Nothing on the network can reach it.
  So it is the safe choice for practice.
- The **port** is a number from 1 to 65535. It selects 1 service on that computer.
  It is like the number of a flat (apartment) in a building.
  Ports below 1024 need root (the administrator user).
  So practice servers use big numbers like `43121`.
  Only 1 program at a time can listen on a port.

### Start a tiny web server

Python comes with a small web server. It shares the files in the current folder:

```bash
python3 -m http.server 43121 --bind 127.0.0.1 > server.log 2>&1 &
echo $! > server.pid
```

- `43121` is the port. `--bind 127.0.0.1` keeps the server on localhost.
- `> server.log 2>&1` sends everything the server prints (normal output and errors) into a log
  file. So the server does not keep control of your terminal or of the output of your script.
- `&` runs the server in the background (you learned this in the Processes challenge).
  So your shell or script can continue.
- `$!` is the PID (process ID number) of the last background command.
  You save it in a **PID file**.
  Later you can stop exactly this server with `kill "$(cat server.pid)"`.

A server needs a short time to start.
In a script, `sleep 1` after you start it is enough here.

### Talk to it with curl

`curl URL` gets a URL (a web address) and prints the answer.
`-s` hides the progress bar.
The URL `http://127.0.0.1:43121/hello.txt` has these parts:

- the language (protocol) `http`,
- the address,
- the port, after the `:`,
- the file to ask for.

```
$ curl -s http://127.0.0.1:43121/hello.txt
hi there
$ curl -s http://127.0.0.1:50000/
$ echo $?
7
```

If nothing listens on that port, curl fails with "Connection refused" and exit code 7.
(The `-s` hides the message.)
So `if curl -s -o /dev/null URL; then ...` tests if a port answers.
`-o /dev/null` throws the page away.

### Which ports are listening?

`ss -ltn` lists the ports that are listening.
The letters mean: `l` listening, `t` TCP (a type of network connection), `n` numbers instead of names.
Look at the Local Address column:

```
$ ss -ltn
State   Recv-Q  Send-Q  Local Address:Port   Peer Address:Port
LISTEN  0       5       127.0.0.1:43121      0.0.0.0:*
```

(`ss` is in the iproute2 package. Raspberry Pi OS has it installed. `./check` does not need it.)

### Logs

A **log** is a text file where a service writes what it is doing. For example:

- when it started,
- which port it used,
- what went wrong.

Read the end of the log with `tail`, or search it:

```bash
tail -n 5 server.log              # the last 5 lines
grep ERROR service.log | tail -n 1   # the most recent error
```

### Config files and restarting

A **config file** holds the settings of a service as text.
Often it has lines like `key=value`.
So you can change the settings without changing the program.
A service reads its config **only when it starts**.
So after you edit the config, you must **restart** the service:
stop the old process, then start a new one.
`sed -i` edits a file in place (it changes the file itself):

```bash
sed -i 's/^port=.*/port=50123/' app.conf   # replace the whole port= line
```

`s/OLD/NEW/` replaces text.
`^` means "start of the line".
`.*` means "anything".

### New words

- service / daemon: a program that keeps running in the background and answers requests.
- listen: wait for connections on an address and port.
- localhost / 127.0.0.1 / loopback: this computer only.
- port: a number that picks one service on a computer.
- PID file: a file that stores the PID of a background process, so you can stop it later.
- curl: a command that fetches a URL and prints the answer.
- log: a text file where a program reports what happened.
- config file: a text file of settings. A program reads it when it starts.
- restart: stop a service, then start it again, so it reads its config again.
- PID: process ID, the number that names a running process.
- URL: a web address, like `http://127.0.0.1:43121/hello.txt`.

## Offline help

- Offline: `man ss`, `man curl`, `help kill`
