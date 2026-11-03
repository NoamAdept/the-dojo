## Compile and Repair a C++ Program

*cpp-compile-it · easy*

**Goal.** Make `meter.cpp` build with no messages under strict warning flags, compute a real average, and print it with exactly one digit after the point, so `./meter` prints `average=20.0`.

**You need to know.**

- The strict build line `g++ -std=c++17 -Wall -Wextra -Werror` and what `-Werror` does (README, "Strict flags").
- Reading `file:line:column` and fixing the first error first (README, "Fix from the top down").
- Operator precedence and brackets (README, "Operator order").
- `std::fixed` and `std::setprecision` from `<iomanip>` (README, "Exactly one digit after the point").

**Walkthrough.**

1. Build once to see all three problems.

   ```bash
   g++ -std=c++17 -Wall -Wextra -Werror meter.cpp -o meter
   ```

   g++ reports `unused variable 'count'` (line 6), `expected ';' before '}' token` (line 12) and `'third' was not declared in this scope` (line 18). Fix them from the top.

2. Task 1 and 2 together: use `count` in `average` and add brackets.

   ```cpp
   double average(double a, double b, double c) {
       int count = 3;
       return (a + b + c) / count;
   }
   ```

   The brackets make the sum happen before the divide, and using `count` removes the unused-variable error. The sum is a `double`, so this is not integer division.

3. Task 1: add the missing `;` at the end of the `std::cout` line in `print_average`. g++ points at the `}` on the next line because that is where it first notices the line never ended.

4. Task 1: give `third` a type in `main`.

   ```cpp
   double third = 30.0;
   ```

   Every variable needs a type the first time it appears.

5. Task 3: print exactly one decimal in `print_average`.

   ```cpp
   void print_average(double value) {
       std::cout << "average=" << std::fixed << std::setprecision(1) << value << std::endl;
   }
   ```

   `std::fixed` forces digits after the point and `std::setprecision(1)` makes it exactly one, so `20` prints as `20.0` and `7.0 / 3` as `2.3`.

6. Build and run.

   ```bash
   g++ -std=c++17 -Wall -Wextra -Werror meter.cpp -o meter && ./meter
   ```

   It prints `average=20.0`.

**Check.** `./check` prints `3/3 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Deleting `int count = 3;` instead of using it. That builds, but then `/ 3` still needs the brackets, and the README asks to use it.
- Writing `a + b + c / count` without brackets: `average(1, 2, 6)` gives 5 instead of 3.
- Looking for the missing `;` on line 12 itself. It belongs at the end of the line above the `}`.
