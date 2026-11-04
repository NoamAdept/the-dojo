# Pipe Dream

`cli-pipeline` · Yellow Belt

**Goal:** From `readings.csv` (columns `callsign,region,strength`), write `answer.txt` with the callsigns of the three strongest `north` stations, strongest first, one per line.

Type in the challenge folder:

```bash
grep ',north,' readings.csv | sort -t, -k3,3nr | head -n 3 | cut -d, -f1 > answer.txt
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
