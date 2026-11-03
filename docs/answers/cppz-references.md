## References: Another Name for a Variable

*cppz-references · easy*

**Goal.** Fill in `plusOne`, `addOne`, `swapValues`, `doubleAll` and `total` in `tasks.h`, seeing the difference between a copy, a reference (`int&`) and a `const` reference.

**You need to know.**

- A normal parameter is a copy: changing it does not touch the caller's variable (README lesson).
- A reference parameter (`int& x`) is another name for the caller's variable, so changes go back to the caller.
- `for (int& x : v)` changes the real items; `for (int x : v)` changes copies.
- A `const std::vector<int>&` can be read but not changed, and is not copied.

**Walkthrough.**

1. Task 1, `plusOne`:

   ```cpp
   return x + 1;
   ```

   `x` is a copy, so the caller's `n` stays 41; the test checks that.

2. Task 2, `addOne` (no return, it is `void`):

   ```cpp
   x = x + 1;
   ```

   Because `x` is `int&`, this line changes the caller's variable itself.

3. Task 3, `swapValues`:

   ```cpp
   int old = a;
   a = b;
   b = old;
   ```

   Save `a` first; otherwise `a = b` overwrites it and both end up with `b`'s value.

4. Task 4, `doubleAll`:

   ```cpp
   for (int& x : v) x = x * 2;
   ```

   The `&` makes `x` a name for each real item in `v`, and `v` itself is passed by reference, so the caller sees the change.

5. Task 5, `total`:

   ```cpp
   int sum = 0;
   for (int x : v) sum += x;
   return sum;
   ```

   Only reading is needed, so a plain `int x` is fine; `const` stops you from changing `v` by mistake.

6. Run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Writing `for (int x : v) x = x * 2;` in `doubleAll`. It compiles but only changes copies, so the vector stays `{1, -4, 10}`.
- Swapping with `a = b; b = a;`, which leaves both as 300.
- Trying to change `v` inside `total`. g++ refuses because `v` is `const`.
