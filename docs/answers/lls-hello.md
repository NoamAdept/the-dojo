## Hello Hackers

*lls-hello · easy*

**Goal.** Write three one-line scripts: run the `hello` command, run it with the single argument `hackers`, and print only the newest line of `~/.bash_history`.

**You need to know.**

- The first word on a line is the command, the rest are arguments (README, commands and arguments).
- `PATH` lists the folders the shell searches for commands; `$DOJO/bin` is added to it for `./try` and `./check`.
- Bash saves your history to `~/.bash_history`, newest command last.
- `tail -n 1 FILE` prints a file's last line.

**Walkthrough.**

1. Try things by hand first.

   ```bash
   . ./env.sh            # sets DOJO and adds $DOJO/bin to PATH
   hello
   ```

   `hello` prints a greeting and a `TOKEN` line. The check reads that token line.

2. Task 1: run the command. In `answers/task1.sh`:

   ```bash
   #!/bin/bash
   hello
   ```

   The shell finds `hello` in a `PATH` folder, so no path is needed.

3. Task 2: one argument. In `answers/task2.sh`:

   ```bash
   #!/bin/bash
   hello hackers
   ```

   The shell splits the line into the command `hello` and one argument `hackers`. `hello` checks that it got exactly that one word (lower case) and prints an `ARG-TOKEN` line.

4. Task 3: newest history entry. In `answers/task3.sh`:

   ```bash
   #!/bin/bash
   tail -n 1 ~/.bash_history
   ```

   `~` becomes the home folder, and `tail -n 1` prints just the last line, which is the most recent command. The check writes its own 41-line history file, so the script must read the file.

5. Test with `./try 1`, `./try 2`, `./try 3`, then run `./check`.

**Check.** `./check` prints `3/3 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `hello Hackers` or `hello hackers now`. `hello` refuses anything but exactly one lower-case `hackers`.
- Copying the last line of the practice history into an `echo`. The check uses a different history, so read the file with `tail`.
- Running `hello` in a fresh terminal without `. ./env.sh` and getting `command not found`. `$DOJO/bin` is only on `PATH` after that step (or inside `./try`).
