## Repeating: while and for

*cpf-loops · easy*

**Goal.** Complete `sum_to`, `factorial`, `count_digits`, `power` and the void function `print_stars` in `tasks.cpp` using `while` and `for` loops.

**You need to know.**

- `while (condition) { ... }` repeats while the condition is true (README lesson on loops).
- `for (int i = 0; i < n; i++) { ... }` runs the body n times.
- The accumulator pattern: start a variable before the loop (0 for sums, 1 for products), update it inside, return it after.
- A `void` function does a job and returns nothing.

**Walkthrough.**

1. Task 1, `sum_to` with a while loop:

   ```cpp
   int total = 0;
   int i = 1;
   while (i <= n) {
       total += i;
       i++;
   }
   return total;
   ```

   `i` walks from 1 to n and each value is added to `total`; for n = 0 the loop never runs and 0 is returned.

2. Task 2, `factorial` with a for loop:

   ```cpp
   int result = 1;
   for (int i = 2; i <= n; i++) {
       result *= i;
   }
   return result;
   ```

   A product starts at 1, so `factorial(0)` and `factorial(1)` give 1 without any special case.

3. Task 3, `count_digits`:

   ```cpp
   int digits = 1;
   while (n >= 10) {
       n /= 10;
       digits++;
   }
   return digits;
   ```

   Every number has at least one digit, and each integer division by 10 removes one more (2024, 202, 20, 2 gives 4).

4. Task 4, `power`:

   ```cpp
   int result = 1;
   for (int i = 0; i < exp; i++) {
       result *= base;
   }
   return result;
   ```

   The loop multiplies by `base` exactly `exp` times; with `exp` 0 it returns 1.

5. Task 5, `print_stars` (the body starts empty):

   ```cpp
   for (int i = 0; i < n; i++) {
       std::cout << '*';
   }
   std::cout << '\n';
   ```

   The star goes inside the loop; the new line goes after it so it is printed once.

6. Build, try, check.

   ```bash
   g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks && ./tasks
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Off-by-one: `while (i < n)` in `sum_to` misses the last number (`sum_to(4)` gives 6).
- Starting a product at 0, which makes every factorial and power 0.
- Putting `std::cout << '\n';` inside the loop, so `print_stars(3)` prints three lines. Or forgetting `i++` in a while loop, which runs forever (the check stops it after 5 seconds).
- Starting `digits` at 0 with `while (n > 0)`: that gives 0 digits for the number 0.
