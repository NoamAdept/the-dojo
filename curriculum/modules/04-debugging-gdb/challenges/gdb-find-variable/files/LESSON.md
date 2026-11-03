# Watch a Variable Change: lesson

A breakpoint can be inside a loop, or in a function that a loop calls. Then the program reaches it once for each trip around the loop.

continue (short: c) lets the program run until the next stop. Each stop prints a "Breakpoint 1, ..." line. You count these lines.

Example: a program calls tick(int n) 3 times, with n = 5, 8, 12.

```
(gdb) break tick
(gdb) run
Breakpoint 1, tick (n=5) at clock.cpp:3        <- stop 1 (first call)
(gdb) continue
Continuing.
Breakpoint 1, tick (n=8) at clock.cpp:3        <- stop 2
(gdb) continue
Continuing.
Breakpoint 1, tick (n=12) at clock.cpp:3       <- stop 3
(gdb) print n
$1 = 12
```

The first stop after run is call number 1. Count carefully. It is easy to be wrong by 1.

These shortcuts help:

```
continue 2          skip ahead: keeps going past the next stop and
                    pauses at the one after (i.e. 2 more stops)
info breakpoints    lists breakpoints and says "breakpoint already hit
                    3 times", a handy way to check your count. It
                    names the function inspect_here(int): C++ adds
                    the parameter types to the name, nothing more
run (again)         restarts from the beginning if you lose track
                    (answer y if GDB asks to start over)
```

Which variables can you see? When the program is paused inside a function, print shows that function's own variables and parameters.

In this target, inspect_here gets the current level as its parameter. This parameter is also called level. So print level works at that stop.

Read the source first. It helps you guess the answer before you check it in GDB. Use cat target.cpp. It has the same kind of range-for loop that you know from C++ First Programs. (for (int sample : samples) visits each item in turn.)

## New words
- **continue**: let the paused program run to the next breakpoint.
- **hit count**: how many times the program has reached a breakpoint.
- **off-by-one**: being wrong by exactly 1 step when counting.
- **parameter**: the name a function uses for a value passed into it.

## Offline help

- Inside GDB: help continue, help info breakpoints
