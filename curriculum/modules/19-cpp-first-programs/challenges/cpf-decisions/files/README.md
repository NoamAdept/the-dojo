# Making Decisions: if and else

**What you will learn:** how to make a program do different things for different inputs.

Is this new for you? Read **LESSON.md** first. Or press **Lesson** in the app.

## Your tasks

Finish the functions in `tasks.cpp`. To build and test them, use `g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks && ./tasks`.

1. `bigger(a, b)` returns the bigger number of a and b. If they are equal, return either one. Example: `bigger(3, 8)` is 8.
2. `is_even(n)` returns `true` if n is even. It returns `false` if n is odd. Example: `is_even(6)` is true. (Zero is even.)
3. `sign(n)` returns 1 for a positive number. It returns -1 for a negative number, and 0 for zero. Use `else if`.
4. `in_range(x, low, high)` returns `true` if x is between low and high. Include both ends. Use `&&`. Example: `in_range(5, 1, 10)` is true.
5. `grade_letter(score)` returns a char:
   - `'A'` for 90 or more,
   - `'B'` for 80 to 89,
   - `'C'` for 70 to 79,
   - `'F'` for any lower score.

## Check your work

You can run `./check` as many times as you want. It lists each task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
