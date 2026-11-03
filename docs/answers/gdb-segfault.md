## Locate and Fix a Segmentation Fault

*gdb-segfault · medium*

**Goal.** Use the AddressSanitizer report and GDB to find the out-of-range read in `largest`, then fix `target.cpp` so it builds cleanly and prints `largest=12`.

**You need to know.**

- How to read an AddressSanitizer report: the kind of error and the first frame in your file (README.txt lesson).
- `break __asan_report_load4` to stop GDB at the moment of the bad read.
- `bt`, `frame N`, `info locals`, and `print values.size()`.
- A loop over a vector must use `i < values.size()`.

**Walkthrough.**

1. Build and run to see the crash.

   ```bash
   ./run
   ```

   ASan prints `heap-buffer-overflow ... READ of size 4`, then `#0 ... in largest ... target.cpp:7` and `#1 ... in main ... target.cpp:14`. So the bad read is on line 7, inside `largest`.

2. Stop GDB at the bad read and look at the locals.

   ```text
   gdb ./target
   (gdb) break __asan_report_load4
   (gdb) run
   (gdb) bt
   #0  __asan::__asan_report_load4 (...)
   #1  ... in largest (values=std::vector of length 4, ...) at target.cpp:7
   #2  ... in main () at target.cpp:14
   (gdb) frame 1
   (gdb) info locals
   i = 4
   best = 12
   (gdb) print values.size()
   $1 = 4
   (gdb) quit
   ```

   Frame 0 is the sanitizer itself, so your code is frame 1. `i` is 4 but the vector only has items 0 to 3, so `values[4]` is one past the end.

3. Fix the loop bound and guard the empty case in `largest`.

   ```cpp
   static int largest(const std::vector<int> &values) {
       if (values.empty()) return 0;  // no samples: nothing to compare
       int best = values[0];
       for (std::size_t i = 1; i < values.size(); ++i) {
           if (values[i] > best) best = values[i];
       }
       return best;
   }
   ```

   `<` stops at the last valid index. The `empty()` check stops `values[0]` from reading a vector with no items.

4. Rebuild, run, and check.

   ```bash
   ./run
   ./check
   ```

   `./run` now prints `largest=12`.

**Check.** `./check` rebuilds with `-Werror` and the sanitizers, runs it, and prints `CHECK_OK`. Then press Done.

**Common mistakes.**

- Looking at frame 0 and seeing only sanitizer code. Use `frame 1` to reach `largest`.
- Changing the loop to start at 0 but keeping `<=`: still reads one past the end.
- Running plain `run` in GDB without the ASan breakpoint: the report prints but the program exits, so there are no locals to inspect.
