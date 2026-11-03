## Find a Changing Variable

*gdb-find-variable · easy*

**Goal.** Stop at `inspect_here` on its fourth call, read `level`, and write that decimal number to `answer.txt`.

**You need to know.**

- `continue` (`c`) runs on to the next breakpoint stop (README.txt, "Lesson").
- The first stop after `run` is call number one.
- `info breakpoints` shows the hit count, a handy way to check your counting.
- `continue N` skips ahead several stops.

**Walkthrough.**

1. Build.

   ```bash
   ./run
   ```

2. Predict the answer from the source (optional but good practice).

   ```bash
   cat target.cpp
   ```

   `level` starts at 10 and the loop adds 3, 7, -2, 9, 4. After the fourth sample it is 10 + 3 + 7 - 2 + 9 = 27.

3. Stop at the fourth call in GDB.

   ```text
   gdb ./target
   (gdb) break inspect_here
   (gdb) run
   Breakpoint 1, inspect_here (level=13) ...     <- call 1
   (gdb) continue
   Breakpoint 1, inspect_here (level=20) ...     <- call 2
   (gdb) continue
   Breakpoint 1, inspect_here (level=18) ...     <- call 3
   (gdb) continue
   Breakpoint 1, inspect_here (level=27) ...     <- call 4
   (gdb) print level
   $1 = 27
   ```

   Each `continue` lets the loop run one more time until `inspect_here` is entered again. `print level` reads the function's parameter, which holds the current level.

4. Confirm the count.

   ```text
   (gdb) info breakpoints
           breakpoint already hit 4 times
   (gdb) quit
   ```

   Answer `y` if GDB asks to kill the program.

5. Save and check.

   ```bash
   echo 27 > answer.txt
   ./check
   ```

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Off by one: continuing four times instead of three (that gives the fifth call, 31).
- Counting the `run` stop as "call zero".
- Reading `level` after the loop ends (the program prints 31) instead of at the fourth stop.
