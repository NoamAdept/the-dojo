# Shell Variables

The shell keeps **variables** (named places that hold a value).
Set one with `NAME=value`. Do not put spaces around `=`.
Use it with `$NAME`.
Before the shell runs the command, it replaces `$NAME` with the value:

```console
$ VAR=1337
$ echo "VAR is $VAR"
VAR is 1337
$ VAR="1337 SAUCE"       # quote values that contain spaces
```

Without quotes, `VAR=1337 SAUCE` would set VAR only for a command named `SAUCE`.
Names and values are case sensitive: `VAR` and `var` are different.

**Export.** Normal variables stay in the current shell.
`export NAME=value` (or `export NAME`) puts the variable in the **environment**.
Child programs (programs that the shell starts) get a copy of the environment.
`env` prints every exported variable, as lines like `NAME=value`.

**Command substitution.** `$(command)` runs the command and puts its output in that place:
`NOW=$(date)`.
Old scripts use backticks for this.
(Backticks look like `` `date` ``, but `$(...)` is easier to read.
You can also put one `$(...)` inside another.)

**read.** `read NAME` reads 1 line from stdin into NAME.
To read the first line of a file, redirect the file into it: `read NAME < some_file`.

For tasks 2, 3, 4, 6, 7 and 8, the check **sources** your script.
This means it runs your script inside its own shell, like `source answers/task2.sh`.
Then it looks at the variables in that shell at the end.
For task 7, the check types `COLLEGE` on the stdin of your script.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Printing variables**: print the value of the variable `FLAG`. (The check sets it.)
2. **Setting variables**: set the variable `PWN` to `COLLEGE`.
3. **Multi-word variables**: set `PWN` to `COLLEGE YEAH`.
4. **Exporting variables**: run `$DOJO/challenge/run`. Before that, set `PWN` to `COLLEGE` and export it. Also set `COLLEGE` to `PWN`, but do NOT export it (so `run` cannot see it).
5. **Printing exported variables**: use `env`, and print only the line for the variable `FLAG`. It must be exactly `FLAG=...`. Do not print similar names such as `FLAGPOLE` or `MYFLAG`.
6. **Storing command output**: store the output of `$DOJO/challenge/secret` in the variable `PWN`.
7. **Reading input**: use `read` to set `PWN` from the line that is typed on stdin.
8. **Reading files**: use `read` to put the first line of `$DOJO/challenge/read_me` into `PWN`. Do it in 1 command.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
