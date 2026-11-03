# Digesting Documentation

A big part of using Linux is finding the right **arguments** (the words you type after a program name) for a program.
Options are special arguments.
They usually start with `-` (short options, like `ls -a`) or `--` (long options, like `--help`).
Some options take their own argument.
For example, in `find -name flag`, the word `flag` belongs to `-name`.

**Man pages.** A man page is the manual for a program. `man yes` shows the manual for `yes`.
The important parts are:

- NAME: a summary in 1 line.
- SYNOPSIS: how to call the program. `[...]` means the part is optional. `...` means you can repeat it.
- DESCRIPTION: every option.
- SEE ALSO: related pages.

Inside `man`:

- Scroll with the arrow keys.
- Search forward with `/word`.
- Go to the next match with `n` (or to the previous match with `N`).
- Quit with `q`.

Man pages are stored under `/usr/share/man`.
You can tell `man` to look in other folders with `MANPATH`.
You can also open a page file directly with `man -l FILE`.
To search *all* pages by topic, use `man -k WORD` (the same as `apropos WORD`).
It searches the NAME lines, but only if your system has built the man database.
If there is no database, plain `grep` over the page files does the same job:

```console
$ grep -rl "wireless" /usr/share/man/man8     # which pages mention wireless?
```

**--help.** Many programs print a short summary of how to use them when you pass `--help` (sometimes `-h`).

**Builtins.** Some commands, like `cd`, `pwd` and `echo`, are built into the shell itself.
They have no program file.
`type cd` says `cd is a shell builtin`.
The `help` builtin lists all of them.
`help cd` shows the documentation for 1 builtin.

The documentation for this challenge is in the practice copy.
First run `. ./env.sh`. Then try
`MANPATH="$DOJO/usr/share/man" man challenge` or `man -l "$DOJO/usr/share/man/man1/challenge.1"`.
If `man` is not installed, use `less` on the same file.
It shows the raw page, and you can still read it.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Learning from documentation**: the documentation for `$DOJO/challenge/challenge` says: "pass it the argument `--giveflag`". Do that.
2. **Learning complex usage**: `challenge --printfile PATH` prints the file at PATH. Use it to print `$DOJO/flag`.
3. **Reading manuals**: read the `challenge` man page (`$DOJO/usr/share/man/man1/challenge.1`). Run `challenge` with the option that prints the *manual* success message.
4. **Searching manuals**: the `challenge-full` man page lists a lot of options. Search it. Run `challenge` with the 1 option that prints the *search* success message.
5. **Searching for manuals**: the folder `$DOJO/usr/local/man/man1` holds man pages with random names. Find every page in that folder with the word `challenge` in its text. Print the path (or name) of each of these pages, 1 on each line. Each time the check runs, it fills the folder with new random pages.
6. **Helpful programs**: `$DOJO/challenge/helpful` has no man page. Read its `--help` output. Run it with the option that prints the success message.
7. **Help for builtins**: `pwd` is a shell builtin. Print its documentation with the `help` builtin.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
