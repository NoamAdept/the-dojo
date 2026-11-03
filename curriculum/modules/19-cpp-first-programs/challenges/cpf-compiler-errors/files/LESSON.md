# Read a Compiler Error: lesson

### Mistakes are normal

Every programmer makes typing mistakes every day. The compiler is very strict. Sometimes your code breaks a rule of C++. Then the compiler does not make a program. It prints an **error message** instead. This message is a clue to help you. It is not a punishment.

### How to read an error

Try it with the first file:

```
$ g++ -std=c++17 -Wall -Wextra oops1.cpp -o oops1
oops1.cpp: In function 'int main()':
oops1.cpp:5:30: error: expected ';' before 'std'
    5 |     std::cout << "Line one\n"
      |                              ^
      |                              ;
    6 |     std::cout << "Line two\n";
      |     ~~~
```

The important line is the line with `error:`. It has 4 parts:

- `oops1.cpp` is the file.
- `5` is the **line number**. The problem is on line 5 of the file.
- `30` is the **column**. It is the number of characters from the left.
- `expected ';' before 'std'` tells you what g++ thinks is wrong.

Below this line, g++ also prints the line of code. It puts a `^` under the problem spot. Here, it suggests that you add a `;`.

Tip: in vim, type `:set number` to show line numbers. Type `:5` to go to line 5. You can also open a file at a line: `vim +5 oops1.cpp`.

### Errors and warnings

- An **error** means that g++ could not build the program at all.
- A **warning** means that g++ built the program, but something looks wrong. Warnings are often real bugs (mistakes in the code). So `./check` treats warnings like errors. It adds the option `-Werror`, which means "warnings are errors".

Always fix the **first** message first. One mistake can confuse g++. Then g++ prints more messages after it. Often all of these messages go away when you fix the first one.

### The 4 common mistakes in this challenge

- A missing `;` at the end of an instruction. g++ often finds it on the next line.
- A standard name with the wrong spelling. For example, `std::cuot` instead of `std::cout`. g++ says that it "is not a member of 'std'". This means the standard library has nothing with this name. g++ often suggests the correct spelling.
- A missing `}`. g++ comes to the end of the file and is still waiting for the `}`. It says "at end of input".
- A word with the wrong spelling. For example, `retrun` instead of `return`. g++ thinks that it is a name you never created. It says "was not declared in this scope".

### New words

- error message: the text where g++ explains why it could not build your program.
- line number: the line of the file where the problem is. The first line is 1.
- column: how far the problem is from the left edge of the line.
- warning: g++ built the program, but it thinks something is probably a mistake.
- syntax: the grammar rules of a programming language.

## Offline help

- Offline: run `man g++`. Then type `/-Wall` and press Enter. This takes you to the part about warnings.
