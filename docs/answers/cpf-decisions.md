## Making Decisions: if and else

*cpf-decisions · easy*

**Goal.** Complete the five functions in `tasks.cpp` (`bigger`, `is_even`, `sign`, `in_range`, `grade_letter`) using comparisons, `if`/`else if`/`else` and `&&`.

**You need to know.**

- Comparisons (`>`, `<`, `>=`, `<=`, `==`, `!=`) give a `bool` (README lesson on decisions).
- `if (...) { } else if (...) { } else { }` runs the first branch whose condition is true.
- `&&` means both conditions must be true; `==` compares while `=` stores.
- `%` gives the remainder, so `n % 2` is 0 for even numbers.

**Walkthrough.**

1. Task 1, in `bigger`: replace `return 0;`.

   ```cpp
   if (a > b) {
       return a;
   } else {
       return b;
   }
   ```

   If `a` is not larger, `b` is larger or equal, so returning `b` covers the equal case too.

2. Task 2, in `is_even`:

   ```cpp
   return n % 2 == 0;
   ```

   The comparison is already true or false, so you can return it directly. This also works for 0 and negative numbers (-10 % 2 is 0).

3. Task 3, in `sign`:

   ```cpp
   if (n > 0) {
       return 1;
   } else if (n < 0) {
       return -1;
   } else {
       return 0;
   }
   ```

   Three cases need a chain; the final `else` catches the only value left, zero.

4. Task 4, in `in_range`:

   ```cpp
   return x >= low && x <= high;
   ```

   `>=` and `<=` include both ends, and `&&` requires both to hold.

5. Task 5, in `grade_letter`:

   ```cpp
   if (score >= 90) {
       return 'A';
   } else if (score >= 80) {
       return 'B';
   } else if (score >= 70) {
       return 'C';
   } else {
       return 'F';
   }
   ```

   Checking from the top down works because C++ stops at the first true branch, so 85 returns `'B'` before reaching the 70 test. Note the single quotes: a `char` uses `'A'`, not `"A"`.

6. Build, try, check.

   ```bash
   g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks && ./tasks
   ./check
   ```

   In `./tasks` the bools print as `1`/`0`; that is normal.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`. It tests edge values such as 0, negatives, both ends of the range and the scores 90, 89, 80, 79, 70, 69.

**Common mistakes.**

- Writing `if (n = 0)` in `sign`. A single `=` stores instead of comparing; `./check` treats the warning as an error ("suggest parentheses around assignment"). Use `==`.
- Using `>` instead of `>=` in `in_range` or `grade_letter`, which gets the boundary values (1, 10, 90, 80, 70) wrong.
- Checking grades from the bottom up (`if (score >= 70)` first), so every good score returns `'C'`.
