## Processes and Jobs

*llp-processes · easy*

**Goal.** Fill in six small bash scripts, `answers/task1.sh` to `answers/task6.sh`, that find, signal, pause, background and inspect processes. `./check` starts its own helper processes and runs each script against them.

**You need to know.**

- `pgrep -f` and `pkill -f` match the whole command line (README, "Listing").
- `kill -INT`, `kill -STOP`, `kill -CONT` send one named signal to a PID (README, "Signals" table).
- `ps -o stat= -p PID` prints the state letter: `S` sleeping, `R` running, `T` stopped.
- `&` starts a background job, `wait` waits for all of them (README, "Jobs").
- `$?` holds the exit code of the last command (README, "Exit codes").

**Walkthrough.**

Each script runs inside a fresh folder that `./check` prepares, so read the input files by plain name (`target.txt`, `pid.txt`). Replace the `# TODO` line in every file, because `./check` treats any file that still contains `TODO` as unfinished.

1. Task 1, find a PID. The target word is in `target.txt`; the decoys use similar words.

   ```bash
   #!/bin/bash
   pgrep -f "$(cat target.txt)"
   ```

   `$(cat target.txt)` turns the file content into the pattern, and `-f` matches it against the full command line, where the word lives.

2. Task 2, kill the right one. Same setup, but end the process.

   ```bash
   #!/bin/bash
   pkill -f "$(cat target.txt)"
   ```

   `pkill` sends `TERM` to every match; the full word is unique, so only the target dies.

3. Task 3, interrupt. Ctrl-C sends `SIGINT`.

   ```bash
   #!/bin/bash
   kill -INT "$(cat pid.txt)"
   ```

   `kill` is really "send a signal"; `-INT` picks the Ctrl-C one instead of the default `TERM`.

4. Task 4, suspend and resume.

   ```bash
   #!/bin/bash
   p=$(cat pid.txt)
   kill -STOP "$p"
   sleep 0.2
   ps -o stat= -p "$p" > state.txt
   kill -CONT "$p"
   ```

   `STOP` freezes the process, the short `sleep` gives the kernel time to show it as `T`, `ps -o stat=` prints just the state with no header, and `CONT` wakes it again.

5. Task 5, background and wait.

   ```bash
   #!/bin/bash
   ./slow.sh A &
   ./slow.sh B &
   wait
   echo done
   ```

   The two `&` lines run at the same time, so the script takes about 1 second instead of 2; `wait` holds until both finish.

6. Task 6, exit codes.

   ```bash
   #!/bin/bash
   ./mystery
   echo $?
   ```

   `$?` must be read on the very next line, because any other command would overwrite it.

7. Run the checker.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and then `CHECK_OK`. Then press Done in the dojo.

**Common mistakes.**

- Using a short pattern like `pkill -f beacon`: it matches every decoy too, and task 2 fails with "you also ended a decoy".
- Reading the state in task 4 without the `sleep 0.2`, or forgetting `kill -CONT`, so the process stays frozen.
- Leaving the `# TODO` comment in a file, or putting anything between `./mystery` and `echo $?`.
