## Loops over Files

*llp-loops · easy*

**Goal.** Fill in `answers/task1.sh` to `answers/task7.sh` so each script loops over the files in a folder given as `$1` and prints names, counts, sizes, hashes or a sorted report. `./check` makes fresh folders with fresh names (some with spaces) every run.

**You need to know.**

- `for f in "$1"/*.txt; do ... done` (README, the for loop section).
- `shopt -s nullglob` makes an empty glob mean "no loop at all" instead of a literal `*.txt`.
- Quote every variable that holds a path: `"$f"`.
- `basename "$f"`, `stat -c %s "$f"`, `sha256sum`, and `$((n + 1))` arithmetic.

**Walkthrough.**

Remove the `# TODO` line from every file. A good habit for the learner: try a loop by hand first (`for f in t/*.txt; do echo "[$f]"; done`) to see where each value starts and ends.

1. Task 1, names of `.txt` files.

   ```bash
   #!/bin/bash
   shopt -s nullglob
   for f in "$1"/*.txt; do
       basename "$f"
   done
   ```

   The quotes go around `$1` only, with the `*` outside, so the folder name stays whole and the star still expands; `basename` drops the folder part.

2. Task 2, count `.log` files (print `0` if none).

   ```bash
   #!/bin/bash
   shopt -s nullglob
   count=0
   for f in "$1"/*.log; do
       count=$((count + 1))
   done
   echo "$count"
   ```

   Without `nullglob` an empty folder would loop once over the literal text `*.log` and print `1`.

3. Task 3, copy each `.txt` to `$2` with `.bak` added.

   ```bash
   #!/bin/bash
   shopt -s nullglob
   for f in "$1"/*.txt; do
       cp "$f" "$2/$(basename "$f").bak"
   done
   ```

   Quoting both `cp` arguments keeps `my notes.txt` as one name instead of two.

4. Task 4, size of one file.

   ```bash
   #!/bin/bash
   stat -c %s "$1"
   ```

   `%s` asks `stat` for the size in bytes only.

5. Task 5, total size of `.dat` files.

   ```bash
   #!/bin/bash
   shopt -s nullglob
   total=0
   for f in "$1"/*.dat; do
       total=$((total + $(stat -c %s "$f")))
   done
   echo "$total"
   ```

   Command substitution gives each file's size, and `$(( ))` adds it to the running total that starts at 0.

6. Task 6, only the sha256 hash.

   ```bash
   #!/bin/bash
   sha256sum "$1" | cut -d' ' -f1
   ```

   `sha256sum` prints `HASH  NAME`; `cut` keeps the first space-separated field.

7. Task 7, `SIZE NAME` sorted smallest first.

   ```bash
   #!/bin/bash
   shopt -s nullglob
   for f in "$1"/*.txt; do
       echo "$(stat -c %s "$f") $(basename "$f")"
   done | sort -n
   ```

   Piping the whole loop into `sort -n` sorts all lines at once, numerically by the size at the start.

8. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `7/7 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Forgetting `shopt -s nullglob`: task 2 prints `1` and task 5 fails on an empty folder.
- Writing `"$1/*.txt"` with the star inside the quotes, so it never expands, or using `$f` without quotes, which splits names with spaces.
- Putting `| sort -n` inside the loop (it sorts one line at a time) instead of after `done`.
