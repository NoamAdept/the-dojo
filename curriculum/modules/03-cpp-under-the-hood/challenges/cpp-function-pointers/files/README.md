# Type Aliases, Function Pointers and Bounds Checks

**What you will learn:**

- how to give a type a new name
- how to pass a function to another function, and call it
- what `void*` is for
- how to check a buffer's bounds safely when you use unsigned numbers

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Fill in `funcs.cpp`. For task 1, also change 1 line of `funcs.hpp`.

1. **Type alias**: in `funcs.hpp`, make `byte` another name for `uint8_t`. Use `using` or `typedef`.
2. **Call through a pointer**: `apply(op, a, b)` calls the function that `op` points at, with `a` and `b`. It returns the result. `apply(add, 2, 3)` is 5.
3. **Return a function**: `pick_op(symbol)` returns:
   - `add` for `'+'`
   - `mul` for `'*'`
   - `nullptr` for anything else
4. **Callback**: `visit_all(values, count, visit, context)` calls `visit(values[i], context)` once for each of the `count` values, in order. It passes `context` along without changing it.
5. **Cast a `void*`**: `update_stats(value, context)` is a visitor. `context` really points at a `stats`. Add 1 to its `count`. Add `value` to its `sum`.
6. **Unsigned sizes**: `bytes_left(size, offset)` returns how many bytes are left after `offset` in a buffer of `size` bytes. It returns `0` when `offset` is at the end or after the end. It must never wrap around.
7. **Bounds check, then read**: `read_be16_at(buf, size, offset, out)` reads the big-endian 16-bit number at `buf[offset]`, `buf[offset + 1]` into `*out`. Then it returns true. Return false, without reading anything, in these cases:
   - `buf` is `nullptr`
   - `out` is `nullptr`
   - fewer than 2 bytes are left at `offset`. This must work even when `offset` is very large.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
