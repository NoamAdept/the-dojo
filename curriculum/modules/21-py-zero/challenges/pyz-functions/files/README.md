# Functions: def and return

**What you will learn:** how to write a function. The function takes values in and gives a result back.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py` with your own code.

1. **double**: `double(n)` returns `n` times 2.
2. **greet**: `greet(name)` returns the string `Hello, NAME!`. For example, `greet("Ada")` returns `"Hello, Ada!"`. Use an f-string.
3. **area**: `area(width, height)` returns `width` times `height`.
4. **to_khz**: `to_khz(hz)` returns the frequency in kHz (divide by 1000). For example, `to_khz(1500)` returns `1.5`.
5. **Fix print vs return**: `average(a, b)` is already written, but it uses `print`. Change it so it **returns** the average of `a` and `b`.
6. **Call your own function**: `quadruple(n)` returns `n` times 4. It calls `double` two times: `double(double(n))`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
