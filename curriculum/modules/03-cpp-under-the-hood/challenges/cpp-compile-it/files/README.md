# Compile and Repair a C++ Program

**What you will learn:**

- how to build with strict warning flags
- how to fix compiler errors from the top down
- how operator order (`*` and `/` before `+` and `-`) changes a result
- how to print a number with exactly one digit after the point

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

`meter.cpp` has 3 functions:

- `average`: the average of 3 numbers
- `print_average`: prints the average
- `main`

Fix the file. Do not rename the functions.

1. **Build clean**: make `g++ -std=c++17 -Wall -Wextra -Werror meter.cpp -o meter` finish with no messages at all. There are 3 problems:
   - a missing `;`
   - a variable used without a type
   - a variable that is made but never used (the best fix is to use it in `average`)
2. **Operator order**: `average(a, b, c)` returns the real average of the 3 numbers. `average(1, 2, 6)` is `3`.
3. **One digit after the point**: `print_average(value)` prints 3 things: `average=`, then the value with exactly 1 digit after the point, then a new line. `print_average(20)` prints `average=20.0`. `print_average(7.0 / 3)` prints `average=2.3`. When this works, `./meter` prints `average=20.0`.

Compile and run after every fix: `g++ -std=c++17 -Wall -Wextra -Werror meter.cpp -o meter && ./meter`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
