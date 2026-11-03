# Fix a Segfault

What you will learn:

- what a crash from a bad memory access is
- how to read an AddressSanitizer report
- how to pause GDB at the exact bad access
- how to look at the variables there with info locals

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
The program crashes. Use GDB to find out why. Then fix target.cpp so it prints largest=12.

## Steps
1. Press Start, then: `./run`  (you see the crash)
2. GDB: run → bt → frame 0 → info locals
   (with ASan: do `break __asan_report_load4` first. Your code is frame 1,
   as the lesson shows.)
3. Fix target.cpp. Rebuild with `./run`. Check that it prints largest=12.
4. Prove it: `./check`, then Press Done
