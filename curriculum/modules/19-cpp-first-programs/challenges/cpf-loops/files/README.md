# Repeating: while and for

**What you will learn:** how to make the computer repeat something many times. You do not need to write it many times.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Finish the functions in `tasks.cpp`. To build and test them, use `g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks && ./tasks`.

1. `sum_to(n)` returns 1 + 2 + ... + n. Use a **while** loop. Example: `sum_to(4)` is 10. When n = 0, the result is 0.
2. `factorial(n)` returns 1 * 2 * ... * n. Use a **for** loop. Example: `factorial(5)` is 120. `factorial(0)` is 1.
3. `count_digits(n)` returns how many digits a number has. The number is 0 or larger. Examples: `count_digits(2024)` is 4. `count_digits(7)` is 1. `count_digits(0)` is 1. Idea: divide by 10 again and again until nothing is left. Count each time.
4. `power(base, exp)` returns base multiplied by itself exp times. Example: `power(2, 10)` is 1024. `power(5, 0)` is 1.
5. `print_stars(n)` is a void function. It prints n `*` characters and then one new line. Example: `print_stars(3)` prints `***` and a new line. `print_stars(0)` prints only the new line.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
