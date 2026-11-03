# References: Another Name for a Variable

**What you will learn:** what a C++ reference is. You will also learn how to use one so that a function can change your variable.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

### How this challenge works

Write your code in `tasks.h`. Every function is already there. Each one has an empty body and a comment that says what it should do. Each file in `tests/` checks one task. `./check` compiles every test with `g++ -std=c++17` and runs it. Then it tells you in plain words what is still wrong.

1. **plusOne**: `x` comes in by value (a copy). Return `x + 1`. The test checks that the caller's variable did not change.
2. **addOne**: `x` is a reference. Add 1 to it. Then the caller's variable changes. The function returns nothing.
3. **swapValues**: swap the two variables. After `swapValues(a, b)`, `a` has the old value of `b`. And `b` has the old value of `a`.
4. **doubleAll**: multiply every item of the vector by 2. Change the items in place (in the vector itself). Use `for (int& x : v)`.
5. **total**: return the sum of the items. The vector comes in as a `const` reference. So you can read it, but you cannot change it.

## Check your work

Run `./check` as many times as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
