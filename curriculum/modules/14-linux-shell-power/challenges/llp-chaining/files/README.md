# Chaining Commands and Scripts

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write each answer as a bash script in `answers/taskN.sh`. `./check` runs it in a folder that has the helper programs named below.

1. **Semicolon**: run `./first`, then `./second`. `./second` must always run, if `./first` succeeds or not.
2. **Success only**: run `./build`. Run `./deploy` only if `./build` succeeded.
3. **Fallback**: run `./primary`. Run `./backup` only if `./primary` failed.
4. **Arguments**: print 2 lines.
   - Line 1: the second argument, a space, then the first argument.
   - Line 2: the number of arguments.
   (`bash task4.sh x y z` prints `y x` then `3`.)
5. **if / else**: does a regular file with the name in `$1` exist? If yes, print `found NAME`. If no, print `missing NAME` and exit with code 1.
6. **elif**: `$1` is a whole number (an integer). Print which group it is in:
   - `negative` (below 0),
   - `zero`,
   - `small` (1 to 9),
   - `large` (10 or more).
7. **Shebang**: create a script `./hello`. It must have a `#!/bin/bash` line and be executable. It prints `Hello, NAME!`, where NAME is its first argument. `./check` runs `./hello` directly, not with bash.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
