# Follow the Stack: lesson

main may call a function, and that function may call another. After each function finishes, the computer must know where to go back to. So it keeps a pile of notes called the call stack.

Each note is a frame. A frame is one function call that has started but has not finished yet. It has its own variables.

- A new call goes on top of the pile.
- When a function returns, its frame is taken off the pile.

Example program: main calls mix, and mix calls bake.

```
main()        starts first, at the bottom of the pile
 └ mix(4)
    └ bake(8) the newest call, on top of the pile
```

backtrace (short: bt) prints the stack while the program is paused. It lists the newest call first, as frame #0:

```
(gdb) break bake
(gdb) run
(gdb) bt
#0  bake (x=8) at st.cpp:2
#1  0x0000555555555177 in mix (x=4) at st.cpp:3
#2  0x000055555555518b in main () at st.cpp:4
```

How to read a line, from left to right:

1. #number
2. sometimes a return address in hex. You can ignore it.
3. the word "in"
4. the function name, with its arguments in brackets
5. the file and line

```
frame #0       innermost: where the program is paused right now
biggest number outermost: where it all started (always main here)
```

So bt lists the calls from innermost to outermost. Read it from the bottom up to get outermost to innermost: main, then mix, then bake. With arrows, you write this as: main -> mix -> bake.

You can select an older frame and look at its variables:

```
(gdb) frame 1
#1  0x0000555555555177 in mix (x=4) at st.cpp:3
(gdb) print x
$1 = 4
```

The code in target.cpp marks each function [[gnu::noinline]]. This tells the compiler "keep this as a real, separate function". So every call shows in the backtrace.

C++ names. In C++, 2 functions can have the same name if their parameters are different. So tools often print the full name with the parameter types. For example:

- capture(int) instead of capture
- main() instead of main

You will see this form in info breakpoints and in AddressSanitizer reports. Some GDB versions also use it in backtraces. It is the same function.

For answer.txt, both forms are accepted. main -> mix -> bake and main() -> mix(int) -> bake(int) both count.

## New words
- **call stack**: the pile of function calls that have started but not finished.
- **frame**: one entry on the call stack (one active function call).
- **backtrace (bt)**: GDB command that prints the call stack.
- **innermost**: the most recent call, frame #0.
- **outermost**: the oldest call, usually main.

## Offline help

- Inside GDB: help backtrace, help frame
