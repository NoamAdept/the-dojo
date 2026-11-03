# Hello, Python: lesson

**Python** is a programming language. In C++ you wrote a `.cpp` file. You compiled it with `g++` into a program.
Then you ran that program. Python has no compile step. A program called the **interpreter** (`python3`)
reads your file. It runs the file line by line, at once. Check that Python is installed:

```console
$ python3 --version
Python 3.11.2
```

(Your number may be different. Any number that starts with 3 is fine.)

**The interactive prompt.** Type `python3` with nothing after it. You get a new prompt, `>>>`. Every line
you type here runs at once, and Python shows the result. This is called the **REPL** (read, evaluate, print, loop).
It is a good calculator. It is also a good place to try things:

```console
$ python3
>>> 2 + 3
5
>>> 7 / 2
3.5
>>> 7 // 2
3
>>> 7 % 2
1
>>> 2 ** 10
1024
>>> exit()
$
```

Be careful: `/` in Python always gives a number with a decimal point. Even `8 / 2` gives `4.0`. This is
different from C++. In C++, `7 / 2` on two ints gives `3`. In Python, the division that drops the remainder is `//`.

- `%` is the remainder (the same as in C++).
- `**` means "to the power of".

Leave the prompt with `exit()` or Ctrl-D.

**A .py file.** For code longer than one line, put the code in a file. The file name ends in `.py`. Then run it:

```console
$ vim hello.py           # press i, type the line below, then Esc and :wq to save and quit
print("Hello!")
$ python3 hello.py
Hello!
```

`print(...)` writes what is inside the brackets to the screen. Then it moves to a new line.
You do not need `\n` or `std::endl`, as you do with `std::cout` in C++.

Text goes in quotes, either `"double"` or `'single'`. Text in quotes is called a **string**. Numbers go without quotes.
Python calculates sums before it prints them. You can give `print` several things, separated by commas. Then it puts
one space between them:

```python
print("Total:", 2 + 3)      # prints: Total: 5
```

Compare this with C++. Some things are missing:

- no `#include`
- no `main()`
- no semicolons
- no braces

The file runs from the top line down. A `#` starts a **comment**. Python ignores everything from `#` to the end of the line.

**Errors.** Sometimes Python cannot understand or run a line. Then it stops and prints an error. The error gives:

- the file name
- the line number
- the kind of problem

For example:

```console
$ python3 oops.py
  File "/home/hacker/oops.py", line 1
    print("hi"
         ^
SyntaxError: '(' was never closed
```

Read the **last line** first. It says what went wrong. Then read the line number. It says where.
This is your main tool for debugging (finding and fixing mistakes).

**New words**
- interpreter: the program (`python3`) that reads and runs Python code directly. There is no compile step.
- REPL: the `>>>` prompt. Each line you type there runs at once.
- string: a piece of text in quotes, like `"Hello"`.
- comment: text after `#`. Python ignores it. It is a note for people.
- SyntaxError: an error. It means a line is not written in correct Python (for example, a bracket is missing).
- debugging: finding and fixing mistakes in code.

## Offline help

- Offline: `python3 -m pydoc print`
