# Loops: for, range and while

**What you will learn:** how to repeat code many times, without writing it out many times.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`.

1. **sum_to**: `sum_to(n)` returns 1 + 2 + ... + n. Use a `for` loop over `range`. `sum_to(0)` is 0.
2. **countdown**: `countdown(n)` returns a string of the numbers from `n` down to 1. Put a space after each number. Then add `liftoff`. For example, `countdown(3)` returns `"3 2 1 liftoff"`.
3. **factorial**: `factorial(n)` returns 1 * 2 * ... * n. `factorial(0)` is 1.
4. **count_multiples**: `count_multiples(n, k)` looks at the numbers 1 to n. It returns how many of them you can divide by `k` with no remainder.
5. **count_digits**: `count_digits(n)` returns how many digits a whole number `n >= 0` has. Use a `while` loop that does `n = n // 10` again and again. `count_digits(0)` is 1.
6. **first_power_over**: `first_power_over(limit)` returns the smallest power of 2 (1, 2, 4, 8, ...) that is **greater than** `limit`. Use a `while` loop.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
