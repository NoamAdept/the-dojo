## Connect Parent and Child with a Pipe

*sys-pipes · medium*

**Goal.** Finish `pipe_demo.cpp` so a child process writes `samples=64` into a pipe, and the parent reads it, prints it once, and waits for the child.

**You need to know.**

- `pipe(fds)` makes a one-way channel: `fds[0]` is the read end, `fds[1]` the write end (`man 2 pipe`, `man 7 pipe`).
- `fork()` returns 0 in the child and the child's pid in the parent (`man 2 fork`).
- `read` only returns 0 (end of data) when every write end is closed.
- `wait(nullptr)` collects the finished child (`man 2 wait`).

**Walkthrough.**

All edits are in `main` in `pipe_demo.cpp`. Replace the TODO comments and the final `return 2;`.

1. TODO 1 and 2: make the pipe, then fork.

   ```cpp
   int fds[2];
   if (pipe(fds) == -1) {
       std::perror("pipe");
       return 1;
   }
   pid_t pid = fork();
   if (pid == -1) {
       std::perror("fork");
       return 1;
   }
   ```

   The pipe must exist before `fork`, so both processes get copies of the same two ends.

2. TODO 3: the child writes.

   ```cpp
   if (pid == 0) {
       close(fds[0]);
       const std::string msg = "samples=64";
       if (write(fds[1], msg.data(), msg.size()) == -1) std::perror("write");
       close(fds[1]);
       _exit(0);
   }
   ```

   The child closes the end it does not use, writes the text, and leaves with `_exit` so it never runs the parent's code below.

3. TODO 4: the parent reads, prints and waits.

   ```cpp
   close(fds[1]);
   std::string text;
   char buf[64];
   ssize_t got;
   while ((got = read(fds[0], buf, sizeof buf)) > 0) {
       text.append(buf, got);
   }
   if (got == -1) std::perror("read");
   close(fds[0]);
   wait(nullptr);
   std::cout << text << '\n';
   return 0;
   ```

   Closing `fds[1]` in the parent is what lets `read` return 0 once the child is done. `append(buf, got)` adds exactly the bytes that arrived.

4. Build and check.

   ```bash
   ./run
   ./check
   ```

   `./run` prints `samples=64`.

**Check.** `./check` runs the program with a 5 second limit, expects exit code 0 and the line `samples=64` exactly once, and prints `CHECK_OK`.

**Common mistakes.**

- The parent forgets `close(fds[1])`: `read` never sees the end, and the program hangs (the checker says so).
- The child returns or falls through instead of calling `_exit(0)`: it also runs the parent's code below, which gives confusing extra output and errors.
- Calling `fork()` before `pipe()`: the two processes get separate pipes and cannot talk.
