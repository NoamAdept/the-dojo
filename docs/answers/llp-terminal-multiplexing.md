## Terminal Multiplexing with tmux

*llp-terminal-multiplexing · medium*

**Goal.** Fill in `answers/task1.sh` to `answers/task6.sh` so each script drives tmux from the command line: start a detached session, list sessions, type into one, add a window, read its screen and kill it.

**You need to know.**

- A tmux session keeps running after you detach (README, sessions section).
- `-d` means detached, `-s NAME` names a new session, `-t NAME` targets an existing one.
- `send-keys ... Enter` types text into a pane as if from the keyboard.
- `capture-pane -p` prints what a pane shows.
- `-F '#S'` is a format that prints only session names.

**Walkthrough.**

The session name lives in `name.txt`, so every script reads it with `"$(cat name.txt)"`. `./check` runs tmux on its own private server, so it never touches a tmux the learner is sitting in. Remove the `# TODO` line in each file.

1. Task 1, start detached.

   ```bash
   #!/bin/bash
   tmux new-session -d -s "$(cat name.txt)"
   ```

   `-d` starts it in the background, which a script needs because there is no terminal to attach to.

2. Task 2, list session names.

   ```bash
   #!/bin/bash
   tmux ls -F '#S'
   ```

   Plain `tmux ls` adds window counts and dates; the `#S` format prints the bare name, one per line.

3. Task 3, send keys.

   ```bash
   #!/bin/bash
   tmux send-keys -t "$(cat name.txt)" "echo $(cat token.txt) > out.txt" Enter
   ```

   The double-quoted string is built first (the token is filled in), then typed into the session; the word `Enter` presses the Enter key so the command runs.

4. Task 4, new window named `logs`.

   ```bash
   #!/bin/bash
   tmux new-window -t "$(cat name.txt)" -n logs
   ```

   `-t` picks the session that gets the window and `-n` names it.

5. Task 5, read the screen.

   ```bash
   #!/bin/bash
   tmux capture-pane -p -t "$(cat name.txt)"
   ```

   `-p` prints the captured pane to standard output instead of saving it in a tmux buffer.

6. Task 6, kill one session.

   ```bash
   #!/bin/bash
   tmux kill-session -t "$(cat name.txt)"
   ```

   `kill-session` ends only the target; `kill-server` would end all of them.

7. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and then `CHECK_OK`. Then press Done.

**Common mistakes.**

- Leaving out `-d` in task 1: the script tries to attach and fails with "not a terminal".
- Forgetting `Enter` in task 3: the text is typed but never run, so `out.txt` never appears.
- Using `tmux kill-server` in task 6, which also kills the sessions that must stay.
