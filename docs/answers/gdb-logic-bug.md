## Debug a Wrong Result

*gdb-logic-bug · medium*

**Goal.** Step through the loop in GDB to see why every sample is counted, then fix the condition in `target.cpp` so samples from 10 to 20 inclusive count and the program prints `usable=4`.

**You need to know.**

- `break LINE` to stop at a source line (README.txt lesson).
- `display EXPR` shows a value at every stop; `next` runs one line.
- `>=` and `<=` for inclusive limits, `&&` for "both must be true".
- Boundary values (10 and 20 here) are where range bugs show up.

**Walkthrough.**

1. Build and run.

   ```bash
   ./run
   ```

   It prints `usable=6`, but only 10, 14, 20 and 17 are in range, so the right answer is 4.

2. Find the line with the `if`.

   ```bash
   grep -n if target.cpp
   ```

   It is line 7.

3. Watch the loop in GDB.

   ```text
   gdb ./target
   (gdb) break 7
   (gdb) run
   (gdb) display i
   (gdb) display samples[i]
   (gdb) display usable
   1: i = 0
   2: samples[i] = 9
   3: usable = 0
   (gdb) next
   8	            usable++;
   ```

   With `samples[i] = 9` the program still goes to `usable++`. That is wrong: 9 is below 10. `9 < 20` is true, and with `||` one true side is enough, so every number passes.

4. Keep going with `continue` and `next` to see 10 and 20 handled, then `quit`.

5. Fix the condition on line 7.

   ```cpp
   if (samples[i] >= 10 && samples[i] <= 20) {
   ```

   `&&` needs both sides true, and `>=`/`<=` include the limits 10 and 20.

6. Rebuild and check.

   ```bash
   ./run
   ./check
   ```

   `./run` prints `usable=4`.

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Changing only `||` to `&&` but keeping `>` and `<`: that gives `usable=2`, because 10 and 20 drop out.
- Changing only `>` to `>=` and `<` to `<=` but keeping `||`: still `usable=6`.
- Setting the breakpoint by function (`break main`) and then stepping through all the setup lines; `break 7` is quicker.
