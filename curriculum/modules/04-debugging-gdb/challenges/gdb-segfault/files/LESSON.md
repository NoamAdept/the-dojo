# Fix a Segfault: lesson

A segmentation fault ("segfault") is a crash. It happens when a program touches memory that it does not own.

A very common cause is reading past the end of a list. A std::vector with 4 items has the valid indexes 0, 1, 2 and 3. Index 4 is outside it. But values[i] does not check the index. It is the fast, low-level way to reach an item. So a small mistake in a loop condition can read garbage (random data), or crash.

```
i < 4    runs i = 0, 1, 2, 3        (4 trips, correct for 4 items)
i <= 4   runs i = 0, 1, 2, 3, 4     (5 trips, one too many)
```

(values.at(i) is the checked version. It throws an error instead. The target uses [] on purpose, so you can practise finding the bug.)

Reading 1 step too far does not always crash. So `./run` builds with -fsanitize=address (AddressSanitizer, "ASan"). ASan watches every memory access. At the first bad access, it stops the program and prints a report.

The report is long. Look for these lines:

```
ERROR: AddressSanitizer: heap-buffer-overflow on address ...
READ of size 4 at ...
    #0 0x... in some_function /path/demo.cpp:7
    #1 0x... in main /path/demo.cpp:15
SUMMARY: AddressSanitizer: heap-buffer-overflow demo.cpp:7 in some_function
```

What these lines mean:

- "heap-buffer-overflow": the program went past the end of a block of memory. The program got this block while it was running. This memory area is called the heap. A std::vector keeps its items in such a block.
- "READ of size 4": the program read 1 int (4 bytes) from a bad place.
- The #0, #1 lines are a backtrace, like GDB's. Frame #0 is where the problem happened.

On some systems, the names have parameter types, like some_function(std::vector<int> const&). It is the same function with a longer C++ name.

Further down there is a second list ("allocated by thread T0 here"). It shows where the vector was created. It is full of std:: library names. You can skip it.

Using GDB. When ASan finds a problem, the program prints its report and exits. So after the crash, bt says "No stack."

The trick: put a breakpoint on ASan's own reporting function. Then GDB pauses just before the report. At that moment, your function is still on the stack:

```
$ gdb ./target
(gdb) break __asan_report_load4
(gdb) run
(gdb) bt
#0  __asan::__asan_report_load4 (...) at .../asan_rtl.cpp:130
#1  0x... in some_function (values=std::vector of length 4, ...) at demo.cpp:7
#2  0x... in main () at demo.cpp:15
```

Frame #0 is ASan itself. You may see a "No such file or directory" warning about it. This is normal. Your code is frame #1. Select it and look around:

```
(gdb) frame 1            make frame 1 the one you are looking at
(gdb) info locals        print every local variable in that frame
(gdb) print values       print a parameter (info locals skips those);
                         GDB shows the vector's length and items
(gdb) print values.size()  call a member function: how many items
(gdb) list               show the source lines around this point
```

Compare the index you see with the number of items. This tells you which loop condition is wrong.

Also think about an empty vector. What would the function do if it got one? (values[0] would not exist either.)

After you edit target.cpp, rebuild and run again with `./run`.

## New words
- **segmentation fault (segfault)**: a crash from touching memory you do not own.
- **out of bounds**: an index outside the array's valid range.
- **AddressSanitizer (ASan)**: a compiler option that catches bad memory use.
- **heap**: memory that a program gets while it runs. A vector's items live there.
- **heap-buffer-overflow**: ASan's name for going past the end of a block of memory the program got while running (a vector's items live there).
- **info locals**: GDB command listing a frame's local variables.
- **frame N**: GDB command that selects stack frame N.
- **list**: GDB command that shows nearby source lines.

## Offline help

- Inside GDB: help info locals, help frame
