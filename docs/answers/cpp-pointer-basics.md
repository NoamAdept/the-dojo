## Pointers: Addresses You Can Follow

*cpp-pointer-basics · easy*

**Goal.** Fill in the four functions in `pointers.cpp` so they change values through pointers, sum a row of ints, and return a pointer (or `nullptr`) to a found item.

**You need to know.**

- `&` gives an address and `*` follows one (README, "Pointers").
- Passing an address lets a function change the caller's variable (README, "Changing the caller's variable").
- A pointer plus a count describes a row of values; `values[i]` and `&values[i]` (README, "A pointer to a row of values").
- `nullptr` as "not found" (README, "nullptr").

**Walkthrough.**

All code goes in `pointers.cpp`. Delete each `// TODO task N` line as you fill that function in, or `./check` keeps saying "not implemented yet". Do not edit `pointers.hpp`.

1. Task 1, `add_one`:

   ```cpp
   void add_one(int* x)
   {
       *x = *x + 1;
   }
   ```

   `*x` is the caller's int, so this reads it, adds 1 and writes it back.

2. Task 2, `swap_ints`:

   ```cpp
   void swap_ints(int* a, int* b)
   {
       int temp = *a;
       *a = *b;
       *b = temp;
   }
   ```

   `temp` parks the first value so it is not lost when `*a` is overwritten.

3. Task 3, `sum_array`:

   ```cpp
   int sum_array(const int* values, std::size_t count)
   {
       int total = 0;
       for (std::size_t i = 0; i < count; i++) {
           total += values[i];
       }
       return total;
   }
   ```

   The loop stops before `count`, so it never reads past the end. When `count` is 0 the loop never runs, so a `nullptr` is never touched. `std::size_t` for `i` avoids a signed/unsigned comparison error.

4. Task 4, `find_value`:

   ```cpp
   int* find_value(int* values, std::size_t count, int wanted)
   {
       for (std::size_t i = 0; i < count; i++) {
           if (values[i] == wanted) {
               return &values[i];
           }
       }
       return nullptr;
   }
   ```

   `&values[i]` is the address of the matching item, so the caller can write through it. Returning inside the loop gives the first match.

5. Run `./check` after each task.

**Check.** `./check` prints `4/4 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `x = x + 1;` (moves the pointer, changes nothing) instead of `*x = *x + 1;`.
- Using `i <= count` in the loop: the sanitizer stops the test with a heap-buffer-overflow.
- Using `int i` with `i < count`: `-Werror` fails on comparing signed and unsigned.
