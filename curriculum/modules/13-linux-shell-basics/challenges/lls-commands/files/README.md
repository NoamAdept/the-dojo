# Comprehending Commands

A small set of commands does most of the daily work:

| command | what it does | example |
|---|---|---|
| `cat F...` | print files (the name comes from con**cat**enate: it can join several files) | `cat notes.txt` |
| `grep TEXT F` | print the lines of F that contain TEXT | `grep error log.txt` |
| `diff A B` | show the lines that are different in two files | `diff old.txt new.txt` |
| `ls [DIR]` | list a directory (`-a` also shows hidden files) | `ls -a ~` |
| `touch F` | create an empty file (or update its time) | `touch /tmp/x` |
| `rm F` | delete a file (there is no trash can!) | `rm /tmp/x` |
| `mv A B` | move or rename | `mv a.txt b.txt` |
| `cp A B` | copy | `cp a.txt backup.txt` |
| `mkdir D` | make a directory | `mkdir /tmp/new` |
| `find DIR -name N` | search DIR and all folders inside it for things named N | `find ~ -name '*.wav'` |
| `ln -s TARGET LINK` | make a symbolic link | `ln -s /tmp/a ~/a` |

**diff** output reads like instructions.
`2c2` means "line 2 changed".
`1a2` means "after line 1, add line 2 of the second file".
Lines that start with `<` come from the first file.
Lines that start with `>` come from the second file.

**Hidden files** are files with a name that starts with a dot, like `.bashrc`.
`ls` does not show them unless you add `-a`.

**Symbolic links** are small files that hold the path of another file.
When a program opens the link, Linux follows it to the target (the file it points to).
`file LINK` or `ls -l` shows where a link points.
Some programs always read one fixed path.
A link at that path can make such a program read a different file.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **cat**: print the contents of `~/flag`.
2. **cat absolute paths**: print `$DOJO/flag`. Use its absolute path (the full path that starts with `/`). (The check runs this script from a different folder.)
3. **more catting**: print `$DOJO/opt/vault/a1/b2/c3/flag`. Use its absolute path.
4. **grep**: `$DOJO/challenge/data.txt` has thousands of lines. Print only the line that contains `academy{`.
5. **diff**: `$DOJO/challenge/decoys_and_real.txt` is the same as `$DOJO/challenge/decoys_only.txt`, plus 1 extra line. Use `diff` on the 2 files. The output must show only that difference.
6. **ls**: list the contents of `$DOJO/challenge`. (One file there has a random name.)
7. **touch**: create 2 empty files, `$DOJO/tmp/pwn` and `$DOJO/tmp/college`.
8. **rm**: delete `~/delete_me`. Do not delete anything else.
9. **mv**: move `$DOJO/flag` to `$DOJO/tmp/hack-the-planet`.
10. **cp**: copy `$DOJO/flag` to `$DOJO/tmp/hack-the-planet`. Keep the original file.
11. **hidden files**: list everything in `$DOJO`. Include the hidden (dot) files.
12. **filesystem quest**: use the practice copy. Start by reading `$DOJO/CLUE`. Follow the clues with `ls` and `cat` until you find the real treasure. Your script must print the contents of that last treasure file. Use its full path.
13. **mkdir**: create the directory `$DOJO/tmp/pwn`. Then create an empty file `college` inside it.
14. **find**: print the absolute path of every file named `flag` anywhere under `$DOJO`. Print 1 path on each line. (The check hides more of these files in random folders.)
15. **ln -s**: `$DOJO/challenge/catflag` prints the file `~/not-the-flag`. Make `~/not-the-flag` a symbolic link to `$DOJO/flag`. Then run `catflag`, so that it prints the flag.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
