# File Globbing

A **glob** is a pattern for file names, like `*.txt`.
Before bash runs a command, it expands (replaces) each glob in the arguments with the matching file names:

| glob | matches | example |
|---|---|---|
| `*` | any number of characters, even 0 (but not `/`, and not a `.` at the start) | `file_*` |
| `?` | exactly one character | `file_?` |
| `[abc]` | one character from the set | `file_[ab]` |
| `[!abc]` or `[^abc]` | one character NOT in the set | `[!p]*` |

```console
$ ls
file_a  file_b  file_cc
$ echo file_?
file_a file_b
$ echo /ho*/*ck*
/home/hacker
```

The program never sees the glob.
It only sees the expanded names, in sorted order.
If nothing matches, the shell passes the glob to the program unchanged.
Globs only work **outside quotes**: `"$DOJO"/ch*` expands, but `"$DOJO/ch*"` does not.
You can mix globs, like `*p*` (any name with a p in it) or `[cep]*`.

**Tab completion** is a related feature that you use while you type.
Type the start of a name and press Tab.
Bash fills in the rest, as far as only 1 name matches.
Press Tab a 2nd time to see a list of the options.
Scripts cannot press Tab.
But bash has a builtin command (a command inside bash itself) called `compgen`.
It prints the same candidates (possible names):

```console
$ compgen -f /usr/sh      # file names completing /usr/sh
/usr/share
$ compgen -c whoa         # command names starting with whoa
whoami
```

`$DOJO/challenge/run` prints the arguments it got, after the shell expanded them.
The check also reads what you typed.
This way it can confirm that you used the right kind of glob.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Matching with \***: use `cd` to go into `$DOJO/challenge` with `cd "$DOJO"/GLOB`. GLOB must use `*` and have 4 characters or fewer. Then run `"$DOJO/challenge/run"`.
2. **Matching with ?**: do the same as task 1. But this time GLOB is the word `challenge`, with every `c` and `l` changed to `?`. Do not use `*`.
3. **Matching with []**: run `cd "$DOJO/challenge/files"`. Then run `"$DOJO/challenge/run"` with 1 `[]` glob argument. It must expand to `file_a`, `file_b`, `file_h` and `file_s`.
4. **Matching paths with []**: do not change directory (stay in your home folder). Run `run` with 1 glob argument. It must expand to the absolute paths of the same 4 files.
5. **Multiple globs**: run `cd "$DOJO/challenge/words"`. Then run `run` with 1 glob. The glob must have 3 characters or fewer and contain 2 `*`. It must match every word with a `p` in it.
6. **Mixing globs**: in the same folder, run `run` with 1 glob. The glob must have 6 characters or fewer and use `[]`. It must match only `challenging`, `educational` and `pwning`.
7. **Exclusionary globbing**: in the same folder, run `run` with 1 glob. It must match every file that does NOT start with `p`, `w` or `n`.
8. **Tab completion**: print the file-name completions for `$DOJO/challenge/pwnc`. Use `compgen -f`. The check gives the file a new name each time it runs.
9. **Multiple completion options**: print every file-name completion for `$DOJO/challenge/tabfiles/pwncollege-f`. Print 1 on each line.
10. **Completing commands**: print the names of the commands on your `PATH` that start with `pwncollege`. Use `compgen -c`. Print each name only 1 time.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
