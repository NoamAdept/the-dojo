# Loops over Files

`llp-loops` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task7.sh` so each script loops over the files in a folder given as `$1` and prints names, counts, sizes, hashes or a sorted report. `./check` makes fresh folders with fresh names (some with spaces) every run.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
shopt -s nullglob
for f in "$1"/*.txt; do
    basename "$f"
done
```

**Task 2**

```bash
shopt -s nullglob
count=0
for f in "$1"/*.log; do
    count=$((count + 1))
done
echo "$count"
```

**Task 3**

```bash
shopt -s nullglob
for f in "$1"/*.txt; do
    cp "$f" "$2/$(basename "$f").bak"
done
```

**Task 4**

```bash
stat -c %s "$1"
```

**Task 5**

```bash
shopt -s nullglob
total=0
for f in "$1"/*.dat; do
    total=$((total + $(stat -c %s "$f")))
done
echo "$total"
```

**Task 6**

```bash
sha256sum "$1" | cut -d' ' -f1
```

**Task 7**

```bash
shopt -s nullglob
for f in "$1"/*.txt; do
    echo "$(stat -c %s "$f") $(basename "$f")"
done | sort -n
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
