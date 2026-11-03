# The Silent Port

What you will learn:

- what a local service, an address and a port are,
- how to read a config file and a log,
- how to talk to a web service with curl.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
A small local web service ("beacon") does not start. Fix its config so
that it listens on localhost. Then prove it works with a health check.
The flag is only in the live /health answer. It is not in the files on
disk.

## What you have

```
service/beaconctl.sh          start / stop / logs
service/config/beacon.conf    broken config (fix this)
service/config/beacon.conf.example   known-good example
service/data/                 data files the service expects
INCIDENT.txt                  short incident note
```

## Steps
1. Press Start in the dojo.

2. Try to start the service:

```
./service/beaconctl.sh start
```

3. If it fails, read why:

```
./service/beaconctl.sh logs
```

4. Compare the broken config with the example. Fix only what is wrong:

```
service/config/beacon.conf
service/config/beacon.conf.example
```

   Common problems: a wrong listen address or port, or a wrong data file
   path.

5. Start the service again. Then ask the live service for its health. Use
   the port from the config:

```
curl -s http://127.0.0.1:PORT/health
```

6. Copy the flag from that JSON. Paste it into the dojo, or press Done.

You do not need root or the Internet. Keep the service on localhost.
