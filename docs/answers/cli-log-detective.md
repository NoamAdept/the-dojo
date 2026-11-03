## Investigate a Receiver Log

*cli-log-detective · easy*

**Goal.** Count the `WARN` lines in `receiver.log` per component and write `report.txt` as `component=count` lines in alphabetical order.

**You need to know.**

- Log lines are space-separated `key=value` fields (README, "Lesson").
- `cut -d' ' -f3` picks a field; `cut -d= -f2` keeps the part after `=`.
- `sort | uniq -c` counts identical lines (they must be sorted first).
- `awk '{print $2 "=" $1}'` reorders the two columns.

**Walkthrough.**

1. Look at the log.

   ```bash
   cat receiver.log
   ```

   Each line is `TIME level=LEVEL component=NAME message=TEXT`. Levels are `INFO`, `WARN` and `ERROR`.

2. Keep only WARN lines.

   ```bash
   grep ' level=WARN ' receiver.log
   ```

   The spaces and `level=` make the match exact, so a message containing "WARN" or an `ERROR` line is not counted.

3. Keep only the component name.

   ```bash
   grep ' level=WARN ' receiver.log | cut -d' ' -f3 | cut -d= -f2
   ```

   Field 3 is `component=audio`; the second `cut` keeps `audio`.

4. Count and format, then save.

   ```bash
   grep ' level=WARN ' receiver.log | cut -d' ' -f3 | cut -d= -f2 | sort | uniq -c | awk '{print $2 "=" $1}' > report.txt
   cat report.txt
   ```

   `sort` groups equal names, `uniq -c` prints `COUNT NAME`, and `awk` flips that into `NAME=COUNT`. The result is `audio=2`, `decoder=1`, `tuner=2`; the alphabetical order comes from the `sort`.

5. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Grepping for just `WARN` or counting the `ERROR` line for audio, which gives `audio=3`.
- Using `uniq -c` without `sort` first; it only merges lines that are next to each other.
- Leaving the `uniq -c` format (`2 audio`) or adding spaces around `=`.
