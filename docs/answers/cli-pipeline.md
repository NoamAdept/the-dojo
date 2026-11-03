## Build Your First Pipeline

*cli-pipeline · easy*

**Goal.** From `readings.csv` (columns `callsign,region,strength`), write `answer.txt` with the callsigns of the three strongest `north` stations, strongest first, one per line.

**You need to know.**

- The pipe `|` feeds one command's output into the next (README, "Lesson").
- `grep` keeps matching lines.
- `sort -t, -k3,3nr` sorts on field 3, comma-separated, as numbers, biggest first.
- `head -n 3` keeps the first three lines; `cut -d, -f1` keeps column 1.
- `>` saves output to a file.

**Walkthrough.**

1. Look at the data.

   ```bash
   cat readings.csv
   ```

   The first line is a header; each other line is one station. Four of them are `north`.

2. Keep only northern rows.

   ```bash
   grep ',north,' readings.csv
   ```

   Including both commas matches the whole region field, so a callsign or another word containing "north" could not sneak in.

3. Sort by strength, strongest first.

   ```bash
   grep ',north,' readings.csv | sort -t, -k3,3nr
   ```

   `-t,` sets the separator, `-k3,3` sorts on field 3 only, `n` compares as numbers and `r` reverses.

4. Take the top three and keep only the callsign, then save.

   ```bash
   grep ',north,' readings.csv | sort -t, -k3,3nr | head -n 3 | cut -d, -f1 > answer.txt
   cat answer.txt
   ```

   The file now reads `ECHO`, `TANGO`, `OSCAR` (strengths 91, 73, 55). Each command in the chain does one small job.

5. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Sorting without `n`: text order is fine here by luck, but it breaks as soon as a value has a different number of digits (for example `100` sorts before `55`).
- Forgetting `r`, which gives the three weakest stations.
- Leaving the whole CSV line in `answer.txt` (forgetting `cut`), or including DELTA, which is strongest overall but in the west.
