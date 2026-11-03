# Shell Automation: lesson

A script is a text file with commands in it. bash runs the commands from
top to bottom. inventory.sh already has the start of a script:

```
#!/bin/bash              "shebang": run this file with bash
set -euo pipefail        stop at the first error instead of carrying on
directory=${1:?Usage...} $1 is the first word typed after the script
                         name; save it in a variable called directory,
                         or stop with the usage message if it is missing
```

So `./inventory.sh` /tmp/caps puts /tmp/caps in $directory.

A for loop repeats commands 1 time for each item. A glob is a pattern
for file names, such as `*.iq`. bash expands it: it replaces the glob
with every file name that matches:

```
for f in "$directory"/*.iq; do
    echo "found: $f"
done
```

Put quotes around every variable. Write "$f", not $f. Here is why: a file
called my file.iq has a space in its name. Without quotes, bash splits
it into 2 words, and the script breaks.

If no file matches, bash keeps the pattern as plain text: `*.iq`. Add
the line `shopt -s nullglob` near the top of your script. Then a pattern
with no match gives no items.

Command substitution $( ... ) runs a command. It puts the output of the
command into your line. Often you save the output in a variable:

```
name=$(basename "$f")       the file name without the folder part
                            basename "d/my file.iq"  gives  my file.iq
size=$(stat -c %s "$f")     the size in bytes (Linux; Mac uses stat -f %z)
```

sha256sum makes a fingerprint of the bytes in a file. This fingerprint is
called a "hash". The same bytes always give the same 64 characters. If
1 byte changes, the hash is completely different. sha256sum prints the
hash, then 2 spaces, then the name:

```
$ sha256sum "d/my file.txt"
98ea6e4f216f2fb4...1107be4  d/my file.txt
```

You only want the first part. You can give the file to sha256sum with <.
Then the name is only a - sign. It is easy to remove with cut -d' ' -f1
or with awk '{print $1}'.

To build a line, use echo "$a,$b,$c". This prints the values with commas
between them. Put > file after done. Then everything the loop prints
goes into that file. Pipe the output through sort first, to put the
lines in order. LC_ALL=C sort sorts by plain character codes. This gives
the same order on every computer.

Make the script runnable with chmod u+x inventory.sh. You only need to do
this 1 time (it may already be done). Test the script on a small folder
of your own. Then run `./check`.

## New words
- **script**: a file of commands that run in order.
- **shebang**: the first line #!... It says which program runs the script.
- **$1**: the first argument given to a script.
- **argument**: a word you type after the command name.
- **for loop**: repeats commands 1 time for each item in a list.
- **glob**: a pattern like `*.iq` that expands to matching file names.
- **quoting**: putting "..." around a variable so spaces do not split it.
- **command substitution**: $(command) is replaced by the output of that command.
- **hash / sha256**: a fingerprint of the contents of a file. It always has the same length.

## Offline help

- man bash        (search with /Looping or /Pathname Expansion)
- man sha256sum
