## Variables and Whole Numbers

*cpf-variables · easy*

**Goal.** Add four `std::cout` lines to `numbers.cpp` that print `apples=`, `total=`, `each=` and `left=` computed from the variables `apples` and `friends`.

**You need to know.**

- An `int` variable has a name, a type and a value (README lesson on variables).
- `std::cout << "text" << value << "\n";` prints several pieces in a row.
- `+`, `/` and `%` on two ints: `/` drops the fraction, `%` gives the remainder.
- Build with `g++ -std=c++17 -Wall -Wextra numbers.cpp -o numbers`, run with `./numbers`.

**Walkthrough.**

1. Open `numbers.cpp`. Leave `int apples = 7;` and `int friends = 3;` exactly as they are. `./check` swaps other numbers (23 and 5, 9 and 9) into those lines to test the code.

2. Task 1, under its comment:

   ```cpp
   std::cout << "apples=" << apples << "\n";
   ```

   The quoted text prints as is, then `<< apples` prints the value stored in the variable.

3. Task 2:

   ```cpp
   std::cout << "total=" << apples + friends << "\n";
   ```

   A calculation can go anywhere a value can; C++ adds first, then prints the result.

4. Task 3:

   ```cpp
   std::cout << "each=" << apples / friends << "\n";
   ```

   Both sides are `int`, so 7 / 3 gives 2 and the fraction is thrown away.

5. Task 4:

   ```cpp
   std::cout << "left=" << apples % friends << "\n";
   ```

   `%` is the remainder: 7 = 2 x 3 + 1, so it gives 1.

6. Build, run and check.

   ```bash
   g++ -std=c++17 -Wall -Wextra numbers.cpp -o numbers
   ./numbers
   ./check
   ```

   `./numbers` prints the given line, then `apples=7`, `total=10`, `each=2`, `left=1`.

**Check.** `./check` prints `4/4 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Typing the answers (`"apples=7"`, `"total=10"`) instead of using the variables. It looks right, but the check uses other numbers and then wants `apples=23`.
- Changing the two starting lines. The check says "keep the line `int apples = 7;` exactly as it was".
- Adding spaces like `apples = 7`. The output must be exactly `apples=7`.
