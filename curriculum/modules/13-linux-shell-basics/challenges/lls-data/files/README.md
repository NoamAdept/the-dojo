# Data Manipulation

Small text tools can change the shape of almost any data.
You connect them with pipes (`|`), so the output of one tool goes into the next tool:

| command | what it does | example |
|---|---|---|
| `tr SET1 SET2` | replace each character of SET1 with the matching one in SET2 | `tr a-z A-Z` (uppercase) |
| `tr -d SET` | delete every character in SET | `tr -d "%"` |
| `head -n N` | keep the first N lines | `head -n 3` |
| `tail -n N` | keep the last N lines | `tail -n 1` |
| `cut -d D -f N` | split each line on D and keep field N | `cut -d " " -f 2` |
| `sort` | sort lines (`-n` numeric, `-r` reverse, `-u` unique) | `sort -u names.txt` |

```console
$ echo PWN.COLLEGE | tr .A-Z _a-z
pwn_college
$ printf "1 a\n2 b\n" | cut -d " " -f 2 | tr -d "\n"
ab
```

`tr` understands escapes (special codes that start with a backslash):

- `"\n"` is a newline. Put it in quotes, so the shell does not remove the backslash.
- `"\\"` is a real backslash.

Ranges like `a-z` save typing.
`tr` matches SET1 and SET2 by position: the 1st character with the 1st, the 2nd with the 2nd, and so on.
So `tr a-zA-Z A-Za-z` swaps upper case and lower case.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

All programs are in `$DOJO/challenge/`.

1. **Translating characters**: `swapcase` prints the secret, but upper case and lower case are swapped. Print the original secret. Use `tr`.
2. **Deleting characters**: `carets` prints the secret with extra `^` and `%` characters mixed in. Print it without them. Use `tr -d`.
3. **Deleting newlines**: `newlines` prints the secret split over many lines. Print it with all newlines removed.
4. **head**: send the output of `pwn` through `head`, so only its first 7 lines go to `college`. (You need 2 pipes and 3 commands.)
5. **cut**: `columns` prints lines like `NUMBER CHARACTER`. Print only the characters (the 2nd field, when you split each line on spaces). Join them into 1 line, with no newlines.
6. **sort**: `$DOJO/challenge/flags.txt` holds 100 fake secrets and 1 real secret. In alphabetical order, the real one comes last. Print only the real one.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
