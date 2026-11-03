## Control a Child Process

*sys-process-controller · medium*

**Goal.** Finish `controller.cpp` so it starts `/bin/echo child_ok` in a child process, waits for it, and prints `child_status=0`.

**You need to know.**

- `fork()` makes a copy of the process; it returns 0 in the child (`man 2 fork`).
- `execl` replaces the child's program and only comes back if it failed (`man 3 exec`).
- `waitpid(pid, &status, 0)` waits for that child (`man 2 waitpid`).
- `WIFEXITED` and `WEXITSTATUS` decode the status number.

**Walkthrough.**

All edits are in `main` in `controller.cpp`. Replace the TODO comments and the final `return 2;`.

1. TODO 1: fork.

   ```cpp
   pid_t pid = fork();
   if (pid == -1) {
       std::perror("fork");
       return 1;
   }
   ```

2. TODO 2: the child becomes `/bin/echo`.

   ```cpp
   if (pid == 0) {
       execl("/bin/echo", "echo", "child_ok", static_cast<char *>(nullptr));
       std::perror("execl");
       _exit(127);
   }
   ```

   The first argument is the program path, then the argument list starting with the program's own name. The `nullptr` marks the end of the list. The lines after `execl` only run if it failed, and `_exit(127)` is the usual "could not run" code.

3. TODO 3: the parent waits and reports.

   ```cpp
   int status;
   if (waitpid(pid, &status, 0) == -1) {
       std::perror("waitpid");
       return 1;
   }
   if (WIFEXITED(status)) {
       std::cout << "child_status=" << WEXITSTATUS(status) << '\n';
       return 0;
   }
   std::cout << "child did not exit normally\n";
   return 1;
   ```

   `waitpid` blocks until the child ends, so `child_ok` is printed before the parent's line. `WEXITSTATUS` pulls the exit code out of `status`.

4. Build and check.

   ```bash
   ./run
   ./check
   ```

   `./run` prints `child_ok` and then `child_status=0`.

**Check.** `./check` expects exit code 0, the line `child_ok` before `child_status=0`, and prints `CHECK_OK`.

**Common mistakes.**

- Leaving out the `static_cast<char *>(nullptr)` at the end of `execl`. It still compiles without a warning here, but the argument list has no end and the child may print junk or crash.
- Printing `status` directly instead of `WEXITSTATUS(status)`. It happens to be 0 here, but `./check` also looks for `WEXITSTATUS(` in the source.
- Printing before calling `waitpid`: `child_status=0` can come out before `child_ok`.
