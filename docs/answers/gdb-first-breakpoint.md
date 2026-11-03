## Stop at Your First Breakpoint

*gdb-first-breakpoint · easy*

**Goal.** Pause `./target` in GDB when `checkpoint` is entered, read its `sample` argument, and write that decimal number alone to `answer.txt`.

**You need to know.**

- Why the program is built with `-g -O0` (README.txt, "Lesson"; `./run` does it).
- The four core GDB commands: `break`, `run`, `print`, `quit`.
- That `(gdb)` is GDB's prompt, not the shell.
- Writing a file with `echo NUMBER > answer.txt`.

**Walkthrough.**

1. Build the program with debug information.

   ```bash
   ./run
   ```

   It prints `Built ./target. Next: gdb ./target`.

2. Start GDB on it. The program does not run yet.

   ```bash
   gdb ./target
   ```

3. Set the breakpoint, run, and read the argument.

   ```text
   (gdb) break checkpoint
   (gdb) run
   Breakpoint 1, checkpoint (sample=73) at target.cpp:3
   (gdb) print sample
   $1 = 73
   (gdb) quit
   ```

   `break checkpoint` pauses as soon as the function is entered, and the stop line already shows the argument in brackets. `print sample` confirms it. If GDB asks "Quit anyway?", answer `y`.

4. Why 73? In `main`, `base` is 17 and `shifted = (17 << 2) + 5`. Shifting left by 2 multiplies by 4, so 68 + 5 = 73. Good to ask the learner to predict it from `cat target.cpp` before using GDB.

5. Write the answer and check.

   ```bash
   echo 73 > answer.txt
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Typing `break checkpoint` in the shell instead of at the `(gdb)` prompt.
- Writing `$1 = 73` or `0x49` into `answer.txt`. It must be the plain decimal number only.
- Forgetting `./run` first, so `gdb ./target` says "No such file or directory".
