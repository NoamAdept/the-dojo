# Terminal Multiplexing with tmux

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. Some tasks have a file `name.txt`. It holds the session name to use.

1. **Start detached**: start a new detached tmux session. Use the name in `name.txt`.
2. **List sessions**: a few sessions are already running. Print their names, one per line.
3. **Send keys**: session `name.txt` is running a shell. Make it run the command `echo TOKEN > out.txt`. TOKEN is the content of `token.txt`.
4. **New window**: add a window named `logs` to session `name.txt`.
5. **Read the screen**: session `name.txt` has printed a secret word. Print what is in its pane.
6. **Kill one**: kill session `name.txt`. Leave every other session running.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
