# Capstone: A Signal Level Report

**What you will learn:** how to put together variables, types, functions, decisions, loops and arguments in one complete tool.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

The function `larger` is already in `report.cpp` as an example. Build and run with:

```
$ g++ -std=c++17 -Wall -Wextra report.cpp -o report
$ ./report -40 -72 -55
```

1. `smaller(a, b)` returns the smaller number of a and b.
2. `is_strong(level)` returns `true` when level is -60 or higher.
3. `average(total, count)` returns total divided by count as a **double**. Do not lose the decimals (the integer-division problem).
4. `main` prints the report exactly as LESSON.md shows it. This is 5 lines. `average` has 2 decimals. Use your functions.
5. `main` checks its input:
   - With no levels, it prints `usage: ./report LEVEL...` and returns 1.
   - If a word is not a number, it prints `not a number: WORD` and returns 1.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
