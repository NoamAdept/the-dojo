# Processes and Jobs

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. `./check` runs it in a new folder. The folder holds the files named below.

1. **Find a PID**: `target.txt` holds a word. Exactly 1 running process has that word in its command line. Other processes are similar decoys. Print the PID of the target process and nothing else.
2. **Kill the right one**: the setup is the same. End the target process. Leave the decoys running.
3. **Interrupt**: `pid.txt` holds a PID. Send that process the signal that Ctrl-C sends.
4. **Suspend and resume**: `pid.txt` holds a PID. Do 3 things:
   - Stop (freeze) the process.
   - While it is stopped, write its `ps -o stat=` state to `state.txt`.
   - Then let it continue.
5. **Background and wait**: run `./slow.sh A` and `./slow.sh B` at the same time. Each one takes 1 second. Wait for both. Then print `done`. The whole script must take much less than 2 seconds.
6. **Exit codes**: run `./mystery`. Then print its exit code as the last line of output.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
