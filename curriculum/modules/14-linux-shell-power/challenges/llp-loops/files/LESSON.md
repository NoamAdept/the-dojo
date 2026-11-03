# Loops over Files: lesson

### The for loop

A **loop** repeats commands. A bash `for` loop runs its body (the commands inside it) once
for every item in a list. It puts the current item in a variable. You choose the name of
the variable:

```bash
for colour in red green blue; do
    echo "I like $colour"
done
```

This prints `I like red`, `I like green`, `I like blue`. `do` starts the body. `done` ends
it.

### Globs: a list of files

A **glob** is a pattern with `*`. Before the command runs, bash replaces the glob with the
file names that match it. `*.txt` means "every name that ends in .txt". Put a folder in
front to look in that folder:

```bash
$ ls caps
a.txt  b.txt  notes.log
$ for f in caps/*.txt; do echo "got $f"; done
got caps/a.txt
got caps/b.txt
```

Look: `$f` also holds the folder part (`caps/a.txt`). Maybe the folder is in a variable.
Then put quotes around the variable, but keep the `*` outside the quotes:
`"$dir"/*.txt`.

### nullglob: when nothing matches

If no file matches, bash keeps the pattern as plain text. So the loop runs **once**, and
`f` is the text `caps/*.log`. You almost never want this. Turn it off with 1 line near the
top of your script:

```bash
shopt -s nullglob     # a glob that matches nothing becomes an empty list
```

### Quoting: names with spaces

A file can have the name `my notes.txt`. Without quotes, bash splits `$f` at the space.
Then `cp $f out/` sees 2 names, `my` and `notes.txt`, and it fails. With quotes, the name
stays in 1 piece. Rule: **always write `"$f"`, never `$f` without quotes.**

### $(...): use a command's output

**Command substitution** runs a command and puts its output into your line:

```bash
name=$(basename "caps/my notes.txt")   # name is: my notes.txt   (folder part removed)
size=$(stat -c %s "caps/a.txt")         # size is the file size in bytes, for example 812
echo "$name is $size bytes"
```

- `basename PATH` prints the last part of a path.
- `stat -c %s FILE` prints the size of the file in bytes.

### Adding numbers

Bash does maths with whole numbers inside `$(( ))`:

```bash
total=0
total=$((total + 5))
echo "$total"      # 5
```

### Fingerprints with sha256sum

`sha256sum FILE` prints a **hash**. A hash is 64 characters that work like a fingerprint
of the bytes in the file. The same bytes always give the same hash. `sha256sum` prints the
hash, then 2 spaces, then the name. `cut -d' ' -f1` keeps only the first field (the part
before the first space):

```bash
$ sha256sum a.txt
2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae  a.txt
$ sha256sum a.txt | cut -d' ' -f1
2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae
```

### Sorting what a loop prints

You can send everything that a loop prints through 1 pipe. Put the pipe after `done`:

```bash
for f in caps/*.txt; do
    echo "$(stat -c %s "$f") $f"
done | sort -n          # -n sorts by number, smallest first
```

### New words

- loop: commands that repeat, once for each item.
- for loop: `for VAR in LIST; do ...; done`.
- body: the commands inside a loop.
- glob: a pattern like `*.txt`. Bash replaces it with the names that match.
- nullglob: a shell option. When nothing matches a glob, the glob becomes nothing.
- quoting: writing `"$f"`, so that spaces do not split a value into pieces.
- command substitution: `$(command)`. Bash replaces it with the output of the command.
- basename: prints a path without its folder part.
- hash: a fingerprint of the contents of a file. It always has the same length.

## Offline help

- Offline: `help for`, `help shopt`, `man stat`, `man sha256sum`
