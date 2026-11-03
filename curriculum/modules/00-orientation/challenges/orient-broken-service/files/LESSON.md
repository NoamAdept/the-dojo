# The Silent Port: lesson

A service is a program that keeps running. It waits for other programs to
ask it things. A service is also called a server. A web service answers
requests that come over HTTP. HTTP is the same language that your web
browser speaks.

Other programs must be able to reach the service. So the service
"listens" on an address and a port:

- **address**: which computer. More exactly, which network connection.
  127.0.0.1 means "this computer only". It is also called localhost or
  loopback. 0.0.0.0 means "every network connection". This includes
  connections that other machines can reach. For safety, this beacon
  listens only on loopback. It refuses every other address.
- **port**: a number from 1 to 65535. It picks one service on that
  computer, like a flat number in a building. Example: 8080.

A config file holds the settings of a program. You can change the
settings without changing the code. This config file uses simple
key=value lines. Lines that start with # are comments. A path in it may
be relative, like data/x.json. A relative path starts from the challenge
folder (the folder where you run the commands).

A log is a text file. A program writes in it what it is doing and what
went wrong. When a service stops right at the start, the log usually
says why:

```
ERROR: something specific went wrong here
```

diff shows the lines that are different in 2 files. Lines marked < come
from the first file. Lines marked > come from the second file:

```
$ diff a.conf b.conf
2c2
< color=bleu
---
> color=blue
```

To edit a file, run vim FILE. Press i to type. Press Esc to stop typing.
Type :wq to save and quit.

curl sends a request to a URL and prints the answer. -s means "silent"
(no progress bar). Look at this URL: http://127.0.0.1:8080/status. It
means:

1. use HTTP,
2. go to address 127.0.0.1,
3. use port 8080,
4. ask for the page /status.

```
$ curl -s http://127.0.0.1:8080/status
{"status": "ok", "uptime": 12}
```

That answer is JSON. JSON is a text format of "name": value pairs inside
{ }. If nothing listens on that port, you get this error:

```
curl: (7) Failed to connect to 127.0.0.1 port 8080: Connection refused
```

ss -ltn lists the ports that something is listening on:

- l = listening,
- t = TCP,
- n = show numbers.

Look for your port in the Local Address column.

Note: the start script gives the secret to the service only 1 time.
Maybe the service runs at last, but /health shows no flag. Then do this:

1. Press Start in the dojo again. This puts a new secret in place.
2. Run `./service/beaconctl.sh` stop.
3. Run `./service/beaconctl.sh` start.

## New words
- **service / server**: a program that keeps running and answers requests.
- **HTTP**: the language web browsers and web servers use.
- **localhost / 127.0.0.1 / loopback**: this computer only.
- **port**: a number that picks one service on a computer.
- **config file**: a text file of settings.
- **log**: a text file where a program reports what happened.
- **curl**: a command that fetches a URL.
- **JSON**: a text format of "name": value pairs.
- **Connection refused**: nothing is listening on that address and port.
- **relative path**: a path that starts from the current folder, not from /.

## Offline help

- man curl
- man ss
- man diff
