## Loops: for, range and while

*pyz-loops · easy*

**Goal.** Write six functions in `tasks.py` that use `for` loops over `range` and `while` loops to add, multiply, count and build text.

**You need to know.**

- `range(start, stop, step)`: the stop is never included (README lesson).
- The accumulator pattern: set before the loop, update inside, `return` after.
- `while condition:` repeats until the condition is false.
- `+=`, `*=`, `//` and `%`.

**Walkthrough.**

1. Open `tasks.py`. Each function follows the same shape: start a variable, loop, return it after the loop (not indented under the `for`).

2. Task 1: `sum_to`.

   ```python
   def sum_to(n):
       total = 0
       for i in range(1, n + 1):
           total += i
       return total
   ```

   `range(1, n + 1)` gives 1 to n because the stop is excluded; for `n = 0` the loop never runs and 0 comes back.

3. Task 2: `countdown`.

   ```python
   def countdown(n):
       text = ""
       for i in range(n, 0, -1):
           text += f"{i} "
       return text + "liftoff"
   ```

   A step of `-1` counts down, and stopping at 0 means 1 is the last number. Each number brings its own trailing space.

4. Task 3: `factorial`.

   ```python
   def factorial(n):
       result = 1
       for i in range(2, n + 1):
           result *= i
       return result
   ```

   A product starts at 1, not 0, which also makes `factorial(0)` equal 1.

5. Task 4: `count_multiples`.

   ```python
   def count_multiples(n, k):
       count = 0
       for i in range(1, n + 1):
           if i % k == 0:
               count += 1
       return count
   ```

   `i % k == 0` means `k` divides `i` with nothing left over.

6. Task 5: `count_digits`, with `while`.

   ```python
   def count_digits(n):
       digits = 1
       while n >= 10:
           n = n // 10
           digits += 1
       return digits
   ```

   Every number has at least one digit; each `// 10` chops one digit off the right.

7. Task 6: `first_power_over`, with `while`.

   ```python
   def first_power_over(limit):
       power = 1
       while power <= limit:
           power *= 2
       return power
   ```

   Keep doubling while the power is not yet greater than the limit, so `first_power_over(8)` is 16.

8. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `6/6 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `range(1, n)` instead of `range(1, n + 1)`: off by one, the last number is missing.
- `return` indented inside the loop, so the function returns after the first pass.
- `while power < limit` in task 6: wrong when the limit is itself a power of 2 (8 should give 16).
