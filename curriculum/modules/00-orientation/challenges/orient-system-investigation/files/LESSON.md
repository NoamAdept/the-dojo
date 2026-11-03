# System Investigation: lesson

This challenge uses what you learned in Broken Service, Permissions and
Process Hunt. Nothing big is new. The skill here is to stay calm and to
test 1 idea at a time.

EchoRelay is not a web service. It speaks plain TCP. A program connects
to its address and port and sends 1 line of text. Then it gets 1 line
back.

TCP is the basic "phone line" between 2 programs. HTTP (the language curl
speaks) is one language that programs speak over TCP. nc (netcat) lets
you speak raw TCP by hand:

```
$ printf 'HELLO\n' | nc -w 2 127.0.0.1 5000
HI THERE
```

That command sends HELLO to port 5000 on this computer. Then it prints
the answer. -w 2 means "stop waiting after 2 seconds". verify.sh does
exactly this. Its address and port are written inside it and do not
change. You may read it with cat. Do not edit it:

```
$ cat echorelay/verify.sh
```

The triage loop. Ask 1 question at a time:

```
Is it running?          ./echorelay/relayctl.sh status
Why did it stop?        ./echorelay/relayctl.sh logs
Is the port listening?  ss -ltn   (look for 127.0.0.1:PORT)
Config right?           diff the config against the .example file
Can it read its files?  ls -l the folder, look at the r letters
```

Nobody can read a file with mode ----------. So the log of the worker
will show "Permission denied". You own the file, so chmod u+r fixes this.
It is the same as in the Permissions challenge.

The program reads its config only when it starts. So after every change,
do 3 things: stop, start, verify. Change only 1 thing at a time. If you
change 2 things and it works, you will not know which change helped.

Note: relayctl.sh gives the secret to the worker only 1 time. Maybe
verify connects at last, but the answer has no flag. Then press Start in
the dojo again. This puts a new secret in place. Then stop the relay and
start it again.

## New words
- **TCP**: a reliable two-way connection between 2 programs.
- **nc (netcat)**: sends and receives raw text over TCP.
- **contract**: the promise that a check expects. Here it is "answer PING on this port".
- **triage**: sorting out problems 1 at a time, the most basic first.
- **worker**: the background program that does the real job of the service.
- **restart**: stop and then start, so that a program reads its config again.

## Offline help

- man nc
- man ss
- man chmod
