## Read a Compiler Error

*cpf-compiler-errors · easy*

**Goal.** Fix the one mistake in each of `oops1.cpp` to `oops4.cpp` so each file compiles and prints its line unchanged.

**You need to know.**

- How to read `file:line:column: error: message` (README, "How to read an error").
- Always fix the first `error:` line first.
- `./check` adds `-Werror`, so warnings count as errors too.
- Show line numbers in vim with `:set number`, and jump to a line with `:5` (or open at it with `vim +5 file.cpp`).

**Walkthrough.**

1. Task 1, `oops1.cpp`. Compile it and read the first error.

   ```bash
   g++ -std=c++17 -Wall -Wextra oops1.cpp -o oops1
   # oops1.cpp:5:30: error: expected ';' before 'std'
   ```

   Line 5 is missing its semicolon at the end. Fix it:

   ```cpp
   std::cout << "Line one\n";
   ```

   g++ notices the problem when it reaches `std` on line 6, but the fix belongs at the end of line 5.

2. Task 2, `oops2.cpp`.

   ```bash
   g++ -std=c++17 -Wall -Wextra oops2.cpp -o oops2
   # oops2.cpp:5:10: error: 'cuot' is not a member of 'std'; did you mean 'cout'?
   ```

   ```cpp
   std::cout << "Spelling matters\n";
   ```

   The standard library has no `cuot`; g++ even suggests the right spelling.

3. Task 3, `oops3.cpp`.

   ```bash
   g++ -std=c++17 -Wall -Wextra oops3.cpp -o oops3
   # oops3.cpp:6:14: error: expected '}' at end of input
   ```

   Add the missing closing brace as the last line of the file, after `return 0;`:

   ```cpp
       return 0;
   }
   ```

   Every `{` needs a `}`; g++ hit the end of the file still waiting for one.

4. Task 4, `oops4.cpp`.

   ```bash
   g++ -std=c++17 -Wall -Wextra oops4.cpp -o oops4
   # oops4.cpp:6:5: error: 'retrun' was not declared in this scope
   ```

   ```cpp
   return 0;
   ```

   g++ did not recognize `retrun` as a keyword, so it guessed it was a name you never created.

5. Run each program once to see it works (`./oops1`, `./oops2`, ...), then run `./check`.

**Check.** `./check` prints `4/4 tasks pass` and then `CHECK_OK`. For any file still broken it shows g++'s first error line plus a plain-English hint.

**Common mistakes.**

- Looking for the missing `;` on line 6 because that is where g++ points. The fix is at the end of the line above.
- Changing the printed text while fixing (for example removing `\n`). The check compares the output exactly.
- Trying to fix every message at once. Fix the first error, compile again, and only then look at the next one.
