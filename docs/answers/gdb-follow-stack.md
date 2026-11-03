## Follow the Call Stack

*gdb-follow-stack · medium*

**Goal.** Stop at `capture`, print a backtrace, and write the call chain from `main` to `capture` (outermost to innermost, joined by ` -> `) in `answer.txt`.

**You need to know.**

- What the call stack and a frame are (README.txt, "Lesson").
- `backtrace` (`bt`) lists frames newest first, as `#0`.
- The biggest frame number is the outermost call, here `main`.
- C++ names like `capture(int)` are the same function and are accepted.

**Walkthrough.**

1. Build.

   ```bash
   ./run
   ```

2. Stop at `capture` and print the stack.

   ```text
   gdb ./target
   (gdb) break capture
   (gdb) run
   (gdb) bt
   #0  capture (x=14) at target.cpp:3
   #1  0x... in demodulate (x=7) at target.cpp:4
   #2  0x... in receive (x=4) at target.cpp:5
   #3  0x... in main () at target.cpp:8
   (gdb) quit
   ```

   Frame `#0` is where the program is paused. The hex numbers are return addresses and can be ignored. The `[[gnu::noinline]]` marks in the source make sure every call gets its own frame.

3. Read it from the bottom up: `main`, `receive`, `demodulate`, `capture`. This matches the source: `main` calls `receive(4)`, which calls `demodulate(7)`, which calls `capture(14)`.

4. Optional: look inside an older frame.

   ```text
   (gdb) frame 2
   (gdb) print x
   $1 = 4
   ```

5. Write the answer and check.

   ```bash
   echo 'main -> receive -> demodulate -> capture' > answer.txt
   ./check
   ```

   The quotes keep the shell from treating `>` inside the text as a redirect.

**Check.** `./check` prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Copying the `bt` order (innermost first). `./check` says "that is innermost first" in that case.
- Running `echo main -> receive ...` without quotes: the shell treats `>` as a redirect and creates a file called `receive`.
- Leaving out `main` or `capture`. Both ends must be included.
