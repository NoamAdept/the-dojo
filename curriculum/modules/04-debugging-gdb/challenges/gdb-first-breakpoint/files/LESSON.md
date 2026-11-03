# First Breakpoint: lesson

A debugger lets you pause a running program and look inside it. You can see 2 things:

- which line the program is on
- what is in each variable

GDB (the GNU Debugger) is the standard debugger on Linux.

GDB needs extra "debug information" in the program. With this information, GDB can match the machine code to your source lines and variable names. The compiler adds it when you use -g. `./run` in this folder does that for you:

```
g++ -std=c++17 -Wall -Wextra -g -O0 target.cpp -o target
```

-O0 turns off optimisation (the compiler's changes that make code faster). So the program runs line by line, exactly as written. No variables are "optimised away" (removed by the compiler).

Start GDB on the program. The program does not run yet:

```
$ gdb ./target
(gdb)
```

(gdb) is GDB's prompt. Type GDB commands there. Do not type shell commands there.

```
break NAME    set a breakpoint: pause when function NAME is entered
              (short form: b NAME). break 12 pauses at line 12.
run           start the program; it runs until a breakpoint (r)
print EXPR    show a variable or expression (p EXPR)
continue      carry on until the next breakpoint (c)
quit          leave GDB (q). If it asks "Quit anyway? (y or n)", type y.
```

Here is a short session with a different C++ program. In this program, the function half(int value) is called with 42:

```
(gdb) break half
Breakpoint 1 at 0x1154: file demo.cpp, line 2.
(gdb) run
Breakpoint 1, half (value=42) at demo.cpp:2
2   static int half(int value){ return value / 2; }
(gdb) print value
$1 = 42
(gdb) print value * 2
$2 = 84
(gdb) print/x value
$3 = 0x2a
```

Look at the line where the program stops. It already shows the arguments in brackets.

$1 and $2 are just GDB's numbers for the results. The value comes after the =.

print/x shows the value in hex. Plain print shows it in decimal. answer.txt needs decimal.

C++ note: some GDB messages show a function with its parameter types, like half(int). One example is info breakpoints. This is just the full C++ name of the same function. break half still works.

Write the answer with echo. For example: echo 42 > answer.txt (use your own number).

## New words
- **debugger**: a tool that pauses a program so you can look inside it.
- **GDB**: the GNU Debugger.
- **debug information (-g)**: data that links machine code to source lines.
- **optimisation**: changes the compiler makes so code runs faster. -O0 turns them off.
- **breakpoint**: a place where the program will pause.
- **argument (of a function)**: a value passed into it, like sample here.
- **(gdb)**: the GDB prompt where you type GDB commands.

## Offline help

- man gdb
- Inside GDB: type help, or help break
