# Receiver Log Noir

`cli-log-detective` · Yellow Belt

**Goal:** Count the `WARN` lines in `receiver.log` per component and write `report.txt` as `component=count` lines in alphabetical order.

Type in the challenge folder:

```bash
grep ' level=WARN ' receiver.log | cut -d' ' -f3 | cut -d= -f2 | sort | uniq -c | awk '{print $2 "=" $1}' > report.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
