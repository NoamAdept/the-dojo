## Functions: Inputs and Outputs

*cpf-functions · easy*

**Goal.** Fill in `add`, `square`, `to_fahrenheit` and `sum_of_squares` in `tasks.cpp`, write a brand new `perimeter` function, and print `perimeter(3, 4) = 14` from `main`.

**You need to know.**

- A function has a return type, a name, parameters in `( )` and a body in `{ }` (README lesson on functions).
- `return value;` hands a value back; the call is replaced by that value.
- A function must be written above the code that calls it.
- One function can call another one you already wrote.

**Walkthrough.**

1. Task 1, in `add`: replace `return 0;`.

   ```cpp
   return a + b;
   ```

   The parameters `a` and `b` hold the values the caller passed in, so the function gives back their sum.

2. Task 2, in `square`:

   ```cpp
   return x * x;
   ```

3. Task 3, in `to_fahrenheit`:

   ```cpp
   return celsius * 9 / 5 + 32;
   ```

   `celsius` is a double, so the whole calculation is done with decimals (37.5 gives 99.5, not 99).

4. Task 4: write the whole function yourself, at the `// Task 4` comment, which is above `main`.

   ```cpp
   int perimeter(int width, int height)
   {
       return 2 * width + 2 * height;
   }
   ```

   Then add one line inside `main`, before `return 0;`:

   ```cpp
   std::cout << "perimeter(3, 4) = " << perimeter(3, 4) << "\n";
   ```

   The first line of the function says it takes two ints and gives back an int; the call in `main` prints its result.

5. Task 5, in `sum_of_squares`:

   ```cpp
   return square(a) + square(b);
   ```

   Reusing `square` means you write the squaring logic once. The check really looks for a call to `square(` here.

6. Build, run and check.

   ```bash
   g++ -std=c++17 -Wall -Wextra tasks.cpp -o tasks
   ./tasks
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`. It calls each function with several values, not just the examples.

**Common mistakes.**

- Writing `perimeter` below `main`. g++ then says `'perimeter' was not declared in this scope`.
- Writing `a * a + b * b` in task 5. The answer is right but task 5 fails because it must call `square`.
- Forgetting the print line in `main` for task 4, or getting its text slightly different from `perimeter(3, 4) = 14`.
