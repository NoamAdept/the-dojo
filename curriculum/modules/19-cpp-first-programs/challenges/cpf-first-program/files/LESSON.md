# Your First C++ Program: lesson

### Programs, source files and compilers

A **program** is a list of instructions. The computer follows these instructions. Every command you used so far is a program, for example `ls` or `grep`.

The processor inside your Raspberry Pi only understands **machine code**. Machine code is long rows of numbers. People do not write these numbers by hand.

Instead, we write a **source file**. A source file is a plain text file. We write it in a **programming language**. A programming language is like a very strict and simple kind of English. This module uses the language **C++**. You say it "C plus plus". C++ source files end in `.cpp`.

A **compiler** is a program that reads your source file. It changes the text into machine code. Then it saves the machine code as a new file. You can run this new file. On Linux, the C++ compiler is called `g++`.

```
hello.cpp  --(g++)-->  hello  --(./hello)-->  Hello, world!
(text you write)       (program)              (what it prints)
```

### The smallest useful C++ program

Open `hello.cpp`. For example, use `vim hello.cpp`. To quit vim, type `:q`. The file looks like this:

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello, world!\n";
    return 0;
}
```

Here is each line:

- `#include <iostream>` means "I want to use the standard tools for input and output". "io" means input/output. `std::cout` comes from here.
- `int main()` starts the **main function**. A **function** is a group of instructions with a name. Every C++ program starts to run at `main`. You will learn what `int` and `()` mean later. For now, copy them exactly.
- `{` and `}` are **braces**. Everything between them is part of `main`.
- `std::cout << "Hello, world!\n";` prints the text between the quote marks. Here are its parts:
  - `std::cout` is the screen. You say it "see-out".
  - `<<` means "send this to it".
  - `std::` means "from the standard library". The standard library is the big box of tools that comes with C++.
  - `\n` means "new line". It is like pressing Enter.
  - The `;` (semicolon) ends the instruction. It is like the full stop at the end of a sentence.
- `return 0;` ends the program. It tells the shell "everything went well". 0 means success.

### Compile and run

Open the terminal in this challenge's folder. Then type:

```
$ g++ -std=c++17 -Wall -Wextra hello.cpp -o hello
$ ./hello
Hello, world!
```

- `g++` is the compiler. `hello.cpp` is the source file that it reads.
- `-o hello` means "write the program to a file called `hello`". The "o" means output.
- `-std=c++17` chooses the 2017 version of C++.
- `-Wall -Wextra` ask g++ to warn you about anything that looks like a mistake.
- `./hello` runs the new program. The `./` means "the program in this folder".

If g++ prints nothing, that is good. It means it worked.

Important: **each time you change `hello.cpp`, you must run g++ again.** When you edit the text, the `hello` program does not change by itself.

### New words

- program: a list of instructions that the computer runs, like `ls`.
- machine code: the numbers that the processor really understands.
- source file: the text file that you write, for example `hello.cpp`.
- programming language: strict rules for how to write instructions. C++ is one.
- compiler: a program that changes a source file into a program (`g++`).
- function: a group of instructions with a name. Every program starts at `main`.
- std::cout: the screen. `std::cout << "text";` prints text. `\n` inside the text means "new line".
- semicolon: the `;` at the end of each instruction.

## Offline help

- Offline manual for g++: `man g++`. Press `q` to quit. Type `/word` to search.
