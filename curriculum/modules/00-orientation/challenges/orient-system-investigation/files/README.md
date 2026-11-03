# System Investigation

What you will learn: how to debug a service that is broken in several
places at the same time. You check 1 thing at a time:

- the process,
- the config,
- the file permissions,
- the port.

You will also meet nc. nc is a tool to send raw text over TCP.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
EchoRelay is broken in more than 1 place. Repair it until verify prints a
flag. The flag is only in the live PING answer. It is not in the scripts
on disk.

## What you have

```
echorelay/relayctl.sh              start / stop / status / logs
echorelay/verify.sh                contract check (do not edit)
echorelay/config/relay.conf        broken config (fix this)
echorelay/config/relay.conf.example   known-good example
echorelay/dropbox/                 token file the worker must read
BRIEFING.md                        short incident note
```

## Steps
1. Press Start in the dojo.

2. Start the service and run the contract check:

```
./echorelay/relayctl.sh start
./echorelay/verify.sh
```

3. When something fails, read why:

```
./echorelay/relayctl.sh logs
```

4. Fix 1 problem at a time. Ask these questions:
   - Is the worker still running? (`./echorelay/relayctl.sh status`)
   - Does the config match the example? (listen port, dropbox path)
   - Can the worker read the token? (`ls -l echorelay/dropbox`)

5. After each fix, restart and check again:

```
./echorelay/relayctl.sh stop
./echorelay/relayctl.sh start
./echorelay/verify.sh
```

6. When verify prints a flag, paste it in the dojo, or press Done.

Do not edit verify.sh. Do not use sudo. You do not need the Internet.
