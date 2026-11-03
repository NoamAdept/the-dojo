# Control a Child Process

**What you will learn:**

- how a process starts a different program with `fork` plus `exec`,
- how the parent waits for it,
- how the parent reads its exit status with `waitpid`.

Are you new to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Goal
Complete `controller.cpp`. It must run `/bin/echo child_ok` in a child process. Then it must check that the exit status is zero.
(`fork` creates the child. `exec` replaces its program. `waitpid` collects the status.)

## Steps
1. Press Start. Then run `./run`.
2. Open `controller.cpp` and finish the TODO comments.
3. Run `./check` until it passes. Then press Done.

Everything is offline, in one workspace. You need no hardware.
