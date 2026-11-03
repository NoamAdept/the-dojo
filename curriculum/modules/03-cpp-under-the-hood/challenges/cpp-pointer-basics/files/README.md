# Pointers: Addresses You Can Follow

**What you will learn:**

- what an address and a pointer are
- how `&` and `*` work
- how a function changes the caller's variable through a pointer
- how a pointer moves along a row of values
- what `nullptr` means

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Fill in the functions in `pointers.cpp`. Do not change `pointers.hpp`.

1. **Write through a pointer**: `add_one(x)` adds 1 to the int that `x` points at.
2. **Swap**: `swap_ints(a, b)` swaps the 2 ints that `a` and `b` point at.
3. **Walk a row of values**: `sum_array(values, count)` returns the sum of the first `count` items. When `count` is 0, it returns 0. In that case `values` may even be `nullptr`, so do not read it.
4. **Return a pointer**: `find_value(values, count, wanted)` looks at the `count` items. It returns a pointer to the first item that equals `wanted`. If no item equals `wanted`, it returns `nullptr`. The caller can then change that item through the pointer.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
