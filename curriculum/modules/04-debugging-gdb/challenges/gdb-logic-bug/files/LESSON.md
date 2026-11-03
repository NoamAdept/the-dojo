# Find a Logic Bug: lesson

A logic bug is code that compiles and runs, but gives the wrong answer. There is no crash to show you where it is. So you watch the program work, one line at a time.

Line breakpoints and stepping:

```
break 7          pause when line 7 is about to run (or break target.cpp:7)
next  (n)        run the current line, pause on the next one
step  (s)        like next, but goes inside a function call
display EXPR     print EXPR automatically after every pause
list  (l)        show the source around where you are
```

GDB steps one source LINE at a time. So it helps when each statement is on its own line. target.cpp is written this way. cat -n target.cpp shows the line numbers. Then you can choose the if line for your breakpoint.

A session looks like this:

```
(gdb) break 7
(gdb) run
(gdb) display i
1: i = 0
(gdb) display samples[i]
2: samples[i] = 9
(gdb) next
...after each next, both values are printed again...
```

Each time, ask yourself: "Should this sample count?" Then check if usable goes up.

Comparisons and logic in C++:

```
a > b     a is bigger than b       a >= b    bigger than or equal
a < b     a is smaller than b      a <= b    smaller than or equal
X && Y    true only if BOTH are true          ("and")
X || Y    true if AT LEAST ONE is true        ("or")
```

Test a range check with numbers at its edges and next to its edges. For example, take "x is between 1 and 5, including both". Try 0, 1, 5 and 6:

```
x >= 1 && x <= 5     0: no   1: yes   5: yes   6: no    (correct)
x >= 1 || x <= 5     every number says yes!   (any number is either
                     at least 1 or at most 5)
```

Edge values are the exact limits. Most range bugs hide there.

## New words
- **logic bug**: code that runs but calculates the wrong answer.
- **next**: run one line, then pause.
- **step**: like next, but goes inside function calls.
- **display**: show an expression after every pause.
- **&& (logical and)**: true only if both sides are true.
- **|| (logical or)**: true if either side is true.
- **inclusive**: the limit values themselves count.
- **edge case**: an input exactly at a limit.

## Offline help

- Inside GDB: help next, help display
