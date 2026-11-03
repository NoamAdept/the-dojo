# Terminal Multiplexing with tmux: lesson

Maybe you connect to a Pi with SSH and start a long recording. If you close the laptop,
the recording stops. A **terminal multiplexer** fixes that. It runs your shells inside a
server process. The server process keeps running when you disconnect. The 2 classic
multiplexers are **tmux** and **GNU screen**. These tasks use tmux.

Is tmux installed? Run `command -v tmux`. If it prints nothing, install tmux with
`sudo apt install tmux`.

**By hand:**

| Action | tmux | screen |
|---|---|---|
| start a new session | `tmux new -s radio` | `screen -S radio` |
| detach (leave it running) | Ctrl-b then d | Ctrl-a then d |
| list sessions | `tmux ls` | `screen -ls` |
| attach again | `tmux attach -t radio` | `screen -r radio` |
| new window | Ctrl-b then c | Ctrl-a then c |
| next window / choose a window | Ctrl-b n, Ctrl-b 0..9 | Ctrl-a n, Ctrl-a 0..9 |

**From a script.** Everything that you can do with keys, you can also do with tmux
commands. This is how you automate tmux (make it work without you):

```bash
tmux new-session -d -s radio           # -d: start detached
tmux ls -F '#S'                        # just the session names
tmux send-keys -t radio 'rtl_test' Enter   # type into it
tmux new-window -t radio -n logs       # add a window named logs
tmux capture-pane -p -t radio          # print what is on its screen
tmux kill-session -t radio             # end it
```

`-t` names the target. The target can be a session (`radio`). It can also be a window
inside a session (`radio:logs`).

`./check` gives every task its own private tmux server. (It sets `TMUX_TMPDIR` to a
temporary folder.) So it never touches your own sessions. The session names come from
files, so read them from the files.

### New words

- **SSH**: a way to log in to another computer over the network and type commands there.
- **terminal multiplexer**: a program that runs many shells inside 1 terminal and keeps
  them running when you leave.
- **session**: a group of windows in tmux. It has a name.
- **window / pane**: a window is like a tab in a session. A pane is one part of a window.
- **detach / attach**: leave a session running in the background / connect to it again.
- **detached**: running in the background, not shown on your screen.
