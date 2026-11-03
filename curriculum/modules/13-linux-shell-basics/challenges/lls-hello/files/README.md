# Hello Hackers

The shell is a program. It reads a line of text and splits it into words. It runs the first word as a
command. The other words are the **arguments** of the command (extra information for it):

```console
$ whoami
hacker
$ echo Hello Hackers!
Hello Hackers!
```

In the second line, `echo` is the command. `Hello` and `Hackers!` are 2 arguments. Commands are
case sensitive. This means capital and small letters are different: `hello` and `HELLO` are
different commands.

**History.** Bash remembers what you type. Press the up arrow to get earlier commands back. Or run
`history` to list them. When the shell exits, it saves that list to `~/.bash_history`. The file has
1 command per line. The newest command is at the bottom. A script cannot press the up arrow, but it
can read that file:

```console
$ tail -n 3 ~/.bash_history     # the last 3 commands
```

`tail -n N FILE` prints the last N lines of a file. `head -n N` prints the first N lines.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Intro to commands**: run the `hello` command with no arguments. It is in `$DOJO/bin`. This folder is on your `PATH` during the check.
2. **Intro to arguments**: run `hello` with exactly 1 argument: `hackers`.
3. **Command history**: print the most recent command saved in `~/.bash_history`. Print only that 1 line.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
