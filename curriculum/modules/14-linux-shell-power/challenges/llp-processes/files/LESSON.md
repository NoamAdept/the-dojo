# Processes and Jobs: lesson

Every running program is a **process**. Each process has a number, its **PID** (process
ID). The shell can do 3 things with processes:

- list them,
- send them **signals** (short messages),
- run them in the foreground or in the background.

**Listing.** `ps -ef` (or `ps aux`) shows every process with its full command line. To find
one process by name, filter the list: `ps -ef | grep sleep`. `pgrep` is simpler and safer:

```bash
pgrep sleep          # PIDs of processes named sleep
pgrep -f "radio.py"  # match against the whole command line
ps -o pid,stat,args -p 1234   # details of one PID
```

**Signals.** `kill` does not only kill. It sends a signal. The default signal is `TERM`,
which means "please exit".

| Signal | Meaning | Keyboard shortcut |
|---|---|---|
| `TERM` | asks the process politely to exit | (none, `kill PID`) |
| `INT`  | interrupt (stop what you are doing) | Ctrl-C |
| `STOP` | freeze the process | Ctrl-Z sends `TSTP`, which is similar |
| `CONT` | unfreeze it (continue) | `fg` / `bg` send it |
| `KILL` | end now; the process cannot catch or ignore it | (none) |

Examples: `kill -INT 1234`, `kill -STOP 1234`, `kill -CONT 1234`.

`pkill -f pattern` sends a signal to every process whose command line matches the pattern.
So make the pattern exact. If not, you also hit a decoy (a process that only looks
similar).

In `ps -o stat`, the letters mean:

- `S`: sleeping (waiting).
- `R`: running.
- `T`: stopped.

**Jobs.** A job is a command that the shell started. If you end a command with `&`, it
starts in the background, and you get your prompt back at once.

- `jobs` lists the jobs.
- `fg` brings a job back to the foreground.
- Ctrl-Z and then `bg` moves a running job to the background.
- `wait` pauses until all background jobs are done.

```bash
sleep 2 & sleep 2 &   # both run at the same time
wait                  # about 2 seconds later, both are finished
```

**Exit codes.** Every command ends with a number. The shell puts it in `$?`.

- `0` means success.
- Any other number means some kind of failure.

Read `$?` at once, because the next command replaces it.

In these tasks, `./check` starts its own helper processes. They are harmless. Each
`answers/taskN.sh` acts on them. `./check` always cleans up after itself.

### New words

- **process**: a program that is running.
- **PID**: process ID, the number that names a process.
- **signal**: a short message that the kernel delivers to a process.
- **foreground / background**: a foreground job uses your terminal. A background job runs
  while you keep typing.
- **job**: a command that the shell started and keeps track of.
- **exit code**: the number a command ends with. 0 means success.
- **decoy**: something that looks like the target but is not the target.
