## Your First C++ Program

*cpf-first-program · easy*

**Goal.** Compile `hello.cpp` into a program called `hello`, then change it so it prints exactly two lines: `Hello, C++!` and `I can compile C++.`, and rebuild it.

**You need to know.**

- What a source file, a compiler and a program are (README, "Programs, source files and compilers").
- The compile command `g++ -std=c++17 -Wall -Wextra hello.cpp -o hello` and running with `./hello`.
- `std::cout << "text\n";` prints a line; the `;` ends the instruction.
- The program file does not update itself: edit, then compile again.

**Walkthrough.**

1. Task 1: build and run the starter file as it is.

   ```bash
   g++ -std=c++17 -Wall -Wextra hello.cpp -o hello
   ./hello
   ```

   g++ reads `hello.cpp` and writes the program `hello` (that is what `-o hello` means). No output from g++ means it worked. `./hello` prints `Hello, world!`.

2. Task 2: open the file with `vim hello.cpp`, press `i`, change only the words inside the quotes, then press `Esc` and type `:wq` Enter.

   ```cpp
   std::cout << "Hello, C++!\n";
   ```

   The text between the quote marks is exactly what gets printed, and `\n` ends the line.

3. Task 3: copy that line and put the copy right under it, above `return 0;`.

   ```cpp
   #include <iostream>

   int main()
   {
       std::cout << "Hello, C++!\n";
       std::cout << "I can compile C++.\n";
       return 0;
   }
   ```

   Instructions in `main` run top to bottom, so the second line is printed after the first.

4. Rebuild and run again. This step is what makes task 1 pass at the end.

   ```bash
   g++ -std=c++17 -Wall -Wextra hello.cpp -o hello
   ./hello
   ./check
   ```

   `./check` compiles a fresh copy of `hello.cpp` and compares its output with your `./hello`, so they must match.

**Check.** `./check` prints `3/3 tasks pass` and then `CHECK_OK`. Press Done; the flag is shown by the dojo.

**Common mistakes.**

- Editing `hello.cpp` but not running g++ again. Task 1 then fails with "you edited hello.cpp but did not compile again".
- Deleting the `\n` or the `;`. Without `\n` both sentences end up on one line; without `;` g++ refuses to compile.
- Small typos in the text, like `Hello C++!` (missing comma) or a missing full stop after `C++.`. The check wants the lines exactly.
