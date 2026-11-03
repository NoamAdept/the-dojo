# Performance and Decorators



## Module 13: Performance & Decorators

Step 1 is to write code that works. Step 2 is to write code that is efficient (fast, and light on memory) and easy to maintain. This module teaches:

- decorators (meta-programming: code that changes other code)
- ways to make code faster (performance optimization)

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Simple logger**: `log_call` prints `Calling <name>` before each call. It keeps the `__name__` of the wrapped function (use `functools.wraps`).
2. **Squares generator**: `squares(n)` yields the squares of the numbers from 0 to n.
3. **TimeIt**: `compare_join(number)` uses `timeit.timeit` to measure the time of 2 pieces of code:
   - `" ".join(["a","b","c"])`
   - `"a" + " " + "b" + " " + "c"`

   It returns `(join_seconds, concat_seconds)`.
4. **Slots**: Write `Point` with `__slots__ = ("x", "y")`. Then, if you try to set a new attribute, Python raises `AttributeError`.
5. **Execution limiter**: `run_max_times(n)` is a decorator. It allows n calls. On call number n+1, it raises `RuntimeError`.
6. **Log file analyzer**: `read_large_file(path)` yields the lines of the file one at a time. Remove the `\n` at the end of each line. `error_lines(path)` returns a generator. It gives only the lines that contain `"ERROR"`.
7. **Optimized structure**: Write `Pixel(r, g, b)` with `__slots__`, and write `sum_red(pixels)`. Then write `slots_saves_memory()`. It returns True when both of these are true:
   - a slotted instance has no `__dict__`
   - a slotted instance is smaller (`sys.getsizeof`) than a plain class instance plus its `__dict__`

## Check your work

Run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
