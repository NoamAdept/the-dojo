# Services, Ports and Logs

`llp-services` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task5.sh` to start a small web server in the background, query a server with curl, find which port is listening, read a port from a log, and change a config then restart a service.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
python3 -m http.server "$(cat port.txt)" --bind 127.0.0.1 > server.log 2>&1 &
echo $! > server.pid
```

**Task 2**

```bash
curl -s "http://127.0.0.1:$(cat port.txt)/status.txt"
```

**Task 3**

```bash
for p in $(cat ports.txt); do
    if curl -s -o /dev/null "http://127.0.0.1:$p/"; then
        echo "$p"
    fi
done
```

**Task 4**

```bash
grep 'listening on' service.log | tail -n 1 | awk -F: '{print $NF}'
```

**Task 5**

```bash
sed -i "s/^port=.*/port=$(cat new_port.txt)/" beacon.conf
./ctl.sh restart
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
