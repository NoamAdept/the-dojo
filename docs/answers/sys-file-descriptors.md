## Copy with File Descriptors

*sys-file-descriptors · easy*

**Goal.** Finish `copy.cpp` so `./copy SOURCE DEST` copies any file byte for byte using the POSIX calls `open`, `read`, `write` and `close`, and returns 1 with a message on any error.

**You need to know.**

- A file descriptor is a small int returned by `open` (`man 2 open`).
- `read` returns the number of bytes read, 0 at end of file, -1 on error (`man 2 read`).
- The open flags `O_RDONLY` and `O_WRONLY | O_CREAT | O_TRUNC` with mode `0644`.
- `std::perror` prints your text plus the reason for the last error.

**Walkthrough.**

All edits are in `main` in `copy.cpp`. Delete the two `(void)` lines and the `return 2;` at the end.

1. TODO 1: check the arguments.

   ```cpp
   if (argc != 3) {
       std::cerr << "usage: ./copy SOURCE DEST\n";
       return 1;
   }
   ```

   `argv[0]` is the program name, so two file names make `argc` equal 3.

2. TODO 2 and 3: open both files.

   ```cpp
   int in = open(argv[1], O_RDONLY);
   if (in == -1) {
       std::perror("open");
       return 1;
   }
   int out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
   if (out == -1) {
       std::perror("open");
       close(in);
       return 1;
   }
   ```

   `O_CREAT` makes the file if it is missing, `O_TRUNC` empties an old longer file first, and `0644` is the permission for a new file. The first fd is closed before giving up so nothing leaks.

3. TODO 4: the copy loop.

   ```cpp
   char buf[4096];
   int result = 0;
   while (true) {
       ssize_t got = read(in, buf, sizeof buf);
       if (got == 0) break;
       if (got == -1) { std::perror("read"); result = 1; break; }
       if (write(out, buf, got) != got) { std::perror("write"); result = 1; break; }
   }
   ```

   `read` may return fewer than 4096 bytes, so `write` must use `got`, not `sizeof buf`. A return of 0 means the end of the file.

4. TODO 5: close and return.

   ```cpp
   close(in);
   if (close(out) == -1) { std::perror("close"); result = 1; }
   return result;
   ```

5. Build, try and check.

   ```bash
   ./run
   ./check
   ```

   `./run` prints `output.txt is an exact copy of input.txt`. Try `./copy nope x` to see `open: No such file or directory`.

**Check.** `./check` copies a 100003-byte binary file over a longer file, creates a new file, tries a missing source and a wrong argument count, and prints `CHECK_OK`.

**Common mistakes.**

- Forgetting `O_TRUNC`: `./check` says the copy has extra old bytes at the end.
- Writing `sizeof buf` bytes every time: the last block adds junk and the copy is the wrong size.
- Leaving `return 2;` or the `(void)` lines in after finishing, or using `std::ifstream` (the checker rejects it).
