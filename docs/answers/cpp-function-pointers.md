## Type Aliases, Function Pointers and Bounds Checks

*cpp-function-pointers · easy*

**Goal.** Add a `byte` type alias to `funcs.hpp` and fill in six functions in `funcs.cpp`: calling and returning function pointers, a callback with a `void*` context, and an overflow-safe bounds check before reading.

**You need to know.**

- `using NAME = TYPE;` (or `typedef`) for type aliases (README lesson).
- The function pointer types `int_op` and `int_visitor` in `funcs.hpp`, and calling a pointer like a function.
- `static_cast<stats*>(context)` to turn a `void*` back into its real type.
- Unsigned `std::size_t` wraps around, so compare before subtracting and never add to an untrusted offset.

**Walkthrough.**

Delete each `// TODO task N` comment as you do the task. Run `./check` after each one.

1. Task 1, in `funcs.hpp` (replace the TODO line):

   ```cpp
   using byte = uint8_t;
   ```

   `byte` is now another name for `uint8_t`, so 255 plus 1 wraps to 0 and `sizeof(byte)` is 1.

2. Task 2, `apply` in `funcs.cpp`:

   ```cpp
   return op(a, b);
   ```

   A function pointer is called exactly like a function name.

3. Task 3, `pick_op`:

   ```cpp
   if (symbol == '+') {
       return add;
   }
   if (symbol == '*') {
       return mul;
   }
   return nullptr;
   ```

   A function name without brackets is its address, which is what `int_op` holds.

4. Task 4, `visit_all`:

   ```cpp
   for (std::size_t i = 0; i < count; i++) {
       visit(values[i], context);
   }
   ```

   `context` is passed along untouched; only the visitor knows what it really points at.

5. Task 5, `update_stats`:

   ```cpp
   stats* s = static_cast<stats*>(context);
   s->count += 1;
   s->sum += value;
   ```

   C++ will not turn a `void*` into a `stats*` by itself, so the cast is required.

6. Task 6, `bytes_left`:

   ```cpp
   if (offset >= size) {
       return 0;
   }
   return size - offset;
   ```

   Checking first means `size - offset` never goes below 0 and wraps to a huge number.

7. Task 7, `read_be16_at`:

   ```cpp
   if (buf == nullptr || out == nullptr || bytes_left(size, offset) < 2) {
       return false;
   }
   *out = static_cast<uint16_t>((buf[offset] << 8) | buf[offset + 1]);
   return true;
   ```

   Using `bytes_left` avoids `offset + 2 > size`, which wraps to 0 when `offset` is `SIZE_MAX - 1` and would let the read through.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing the bounds test as `offset + 2 > size`: the `SIZE_MAX-1` case fails, because the addition wraps around.
- Returning `add()` or `&add()` in `pick_op` instead of plain `add`.
- Forgetting task 1 is in the header, not the `.cpp` file.
