# Running Programs and Reading Errors

**What you will learn:**

- how to run a program that is in the current folder
- what the 3 most common error messages mean
- how to read what `./check` tells you

New to this? Read **LESSON.md** first. You can also press **Lesson** in the app.

## Your tasks

1. **Run a program here**: first type `greet` with no `./`. Read the error. Then run it the right way with `./greet`. Save its output into `greet.txt`.
2. **Permission denied**: try `./locked`. Fix the problem with `chmod`. Then save the output of `./locked` into `locked.txt`.
3. **No such file or directory**: run `./report` and read the error. Create what it needs: a folder `data` with a file `settings.txt` inside. The file must contain 1 line: `volume=7`. Then save the output of `./report` into `report.txt`.
4. **Follow the checker**: `./checkme` checks `config.txt`. It prints 1 problem at a time. Fix `config.txt` with vim. Run `./checkme` again. Repeat until it prints `ALL GOOD`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
