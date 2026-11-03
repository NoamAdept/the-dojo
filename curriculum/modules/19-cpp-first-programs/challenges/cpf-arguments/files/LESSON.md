# Input from the Command Line: lesson

### argc and argv

Imagine that you type `./greet Ada`. The shell starts the program and gives it the words. To get these words, write `main` like this, and not as `int main()`:

```cpp
int main(int argc, char* argv[])
```

- `argc` means "argument count". It is an int. It tells how many words were typed. This number **includes the name of the program**.
- `argv` means "argument values". It holds the words.
  - `argv[0]` is the name of the program.
  - `argv[1]` is the first word after the name.
  - `argv[2]` is the second word, and so on.
- Read `char* argv[]` as "the list of words". A later module explains what the `*` and `[]` mean.

For `./greet Ada Lovelace`:

```
argc    = 3
argv[0] = ./greet
argv[1] = Ada
argv[2] = Lovelace
```

You can print a word with std::cout, like any text:

```cpp
std::cout << "Program: " << argv[0] << "\n";
if (argc > 1) {
    std::cout << "First word: " << argv[1] << "\n";
}
```

Always check `argc` before you use `argv[1]`. If the user typed no words, there is no `argv[1]`. If you use it anyway, the program can crash.

The number in the brackets can be a variable. So a loop can visit every word: `argv[i]` is word number i.

### Words to numbers: std::stoi

Every word is text. This is true even in `./add 3 4`. Here argv[1] is the text `3`. It is not the number 3. To change text into a number, use `std::stoi`. The name means "string to int". It needs `#include <string>`:

```cpp
int x = std::stoi(argv[1]);   // the text "3" becomes the number 3
```

### When the word is not a number

Sometimes the word is not a number at all, for example `abc`. Then std::stoi stops and reports a problem. We say that it **throws an exception**. An exception is how C++ says "I cannot do this". If no code catches the exception, the program stops with an ugly crash message.

You can handle the problem yourself:

- Put the risky line in a `try` block.
- In a `catch` block, write what to do instead.

```cpp
int x = 0;
try {
    x = std::stoi(argv[1]);
} catch (...) {
    std::cout << "not a number: " << argv[1] << "\n";
    return 1;
}
```

`catch (...)` means "catch any problem". (std::stoi only reads the start of a word. So `12abc` gives 12. That is OK for now.)

### Exit status

The number that `main` returns is the program's **exit status**. You saw it in the shell modules with `echo $?`. 0 means success. Any other number means that something went wrong.

A good program checks its input. When the input is wrong, it prints a short **usage message**. This message shows how to run the program. Then the program returns 1:

```
$ ./greet
usage: ./greet NAME
$ echo $?
1
```

### New words

- command-line argument: a word that you type after the name of the program.
- argc: how many words there are. It counts the name of the program too.
- argv: the words. argv[0] is the name of the program. argv[1] is the first word after it.
- std::stoi: changes text like "42" into the int 42. It needs `#include <string>`.
- exception: how a function in C++ says "I cannot do this".
- try / catch: run risky code in `try`. If it throws an exception, the `catch` block runs.
- exit status: the number that main returns. 0 means success.
- usage message: one line that reminds the user how to run a program.
