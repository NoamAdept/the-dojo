# Terminal Multiplexing with tmux

`llp-terminal-multiplexing` · Yellow Belt

**Goal:** Fill in `answers/task1.sh` to `answers/task6.sh` so each script drives tmux from the command line: start a detached session, list sessions, type into one, add a window, read its screen and kill it.

Put each answer in `answers/taskN.sh`, in place of the `TODO` line.

**Task 1**

```bash
tmux new-session -d -s "$(cat name.txt)"
```

**Task 2**

```bash
tmux ls -F '#S'
```

**Task 3**

```bash
tmux send-keys -t "$(cat name.txt)" "echo $(cat token.txt) > out.txt" Enter
```

**Task 4**

```bash
tmux new-window -t "$(cat name.txt)" -n logs
```

**Task 5**

```bash
tmux capture-pane -p -t "$(cat name.txt)"
```

**Task 6**

```bash
tmux kill-session -t "$(cat name.txt)"
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
