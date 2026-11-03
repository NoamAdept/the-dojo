## Input from the Command Line

*cpf-arguments · easy*

**Goal.** Finish two programs: `greet.cpp` (`./greet NAME` prints `Hello, NAME!`, with a usage message when no name is given) and `add.cpp` (adds any number of whole numbers and rejects words that are not numbers).

**You need to know.**

- `int main(int argc, char* argv[])`: `argc` counts the words including the program name, `argv[1]` is the first word after it (README lesson).
- Check `argc` before touching `argv[1]`, or the program can crash.
- `std::stoi` (from `<string>`) turns text into an int and throws an exception if the text is not a number.
- `try { } catch (...) { }` catches that exception; `return 1;` from main means "failed".

**Walkthrough.**

1. Tasks 1 and 2, the whole body of `main` in `greet.cpp`:

   ```cpp
   if (argc < 2) {
       std::cout << "usage: ./greet NAME\n";
       return 1;
   }
   std::cout << "Hello, " << argv[1] << "!\n";
   return 0;
   ```

   With no name `argc` is 1, so the check runs first and stops the program with status 1 before `argv[1]` is used. Extra words are simply ignored because only `argv[1]` is printed.

2. Try it:

   ```bash
   g++ -std=c++17 -Wall -Wextra greet.cpp -o greet
   ./greet Ada            # Hello, Ada!
   ./greet; echo $?       # usage line, then 1
   ```

3. Task 3 could be done with `std::stoi(argv[1]) + std::stoi(argv[2])`, but task 4 replaces it, so go straight to the loop. Tasks 3 and 4 in `add.cpp`:

   ```cpp
   int total = 0;
   for (int i = 1; i < argc; i++) {
       total += std::stoi(argv[i]);
   }
   std::cout << total << "\n";
   return 0;
   ```

   The loop starts at 1 to skip the program name and stops before `argc`; with no numbers it never runs and prints 0.

4. Task 5: wrap the conversion in try/catch. Final `main` body of `add.cpp`:

   ```cpp
   int total = 0;
   for (int i = 1; i < argc; i++) {
       try {
           total += std::stoi(argv[i]);
       } catch (...) {
           std::cout << "not a number: " << argv[i] << "\n";
           return 1;
       }
   }
   std::cout << total << "\n";
   return 0;
   ```

   When `std::stoi` cannot read a number it throws, the `catch` block prints the bad word and `return 1;` ends the program before the total is printed.

5. Try it and check:

   ```bash
   g++ -std=c++17 -Wall -Wextra add.cpp -o add
   ./add 1 2 3 4          # 10
   ./add                  # 0
   ./add 3 abc; echo $?   # not a number: abc, then 1
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`. It also checks the exit status (0 or 1) of each run.

**Common mistakes.**

- Using `argv[1]` before checking `argc`. With no name the program crashes; the check reports "the program crashed (signal ...)".
- Starting the add loop at `i = 0`, which tries to convert the program name `./add` and prints `not a number: ./add`.
- Printing the total inside the loop, or printing it even after a bad word. Only one line should come out.
