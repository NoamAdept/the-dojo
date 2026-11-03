## Performance and Decorators

*pyq-performance · medium*

**Goal.** Write decorators (a logger and a call limiter), generators for lazy processing, a `timeit` comparison, and `__slots__` classes that save memory, all in `tasks.py`.

**You need to know.**

- Decorators with `functools.wraps`, and `nonlocal` for state in the enclosing function.
- A function with `yield` returns a generator; a `( ... for ... )` expression is also a generator.
- `timeit.timeit(stmt, number=n)`.
- `__slots__` removes the per-instance `__dict__`; `sys.getsizeof` measures one object.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1. `functools.wraps` copies `__name__` from the original, so `tune.__name__` stays `"tune"`.

   ```python
   def log_call(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           print(f"Calling {func.__name__}")
           return func(*args, **kwargs)
       return wrapper
   ```

3. Task 2. `range(n + 1)` includes `n`; `yield` makes this a generator.

   ```python
   def squares(n):
       for i in range(n + 1):
           yield i * i
   ```

4. Task 3. `timeit` takes the code as a string and runs it `number` times.

   ```python
   def compare_join(number=100_000):
       join = timeit.timeit('" ".join(["a", "b", "c"])', number=number)
       concat = timeit.timeit('"a" + " " + "b" + " " + "c"', number=number)
       return join, concat
   ```

5. Task 4. With `__slots__`, only `x` and `y` can be set.

   ```python
   class Point:
       __slots__ = ("x", "y")
   ```

6. Task 5. A decorator factory with a counter. `nonlocal` lets `wrapper` update `calls`, which lives in `decorator`.

   ```python
   def run_max_times(n):
       def decorator(func):
           calls = 0
           @functools.wraps(func)
           def wrapper(*args, **kwargs):
               nonlocal calls
               if calls >= n:
                   raise RuntimeError(f"{func.__name__} may only run {n} times")
               calls += 1
               return func(*args, **kwargs)
           return wrapper
       return decorator
   ```

7. Task 6. `for line in fh` reads one line at a time. `error_lines` must return a generator expression, not a list.

   ```python
   def read_large_file(path):
       with open(path) as fh:
           for line in fh:
               yield line.rstrip("\n")

   def error_lines(path):
       return (line for line in read_large_file(path) if "ERROR" in line)
   ```

8. Task 7. A slotted `Pixel`, a sum, and a comparison against a plain class. A plain instance's real cost is the object plus its `__dict__`.

   ```python
   class Pixel:
       __slots__ = ("r", "g", "b")
       def __init__(self, r, g, b):
           self.r, self.g, self.b = r, g, b

   def sum_red(pixels):
       return sum(p.r for p in pixels)

   class _PlainPixel:
       def __init__(self, r, g, b):
           self.r, self.g, self.b = r, g, b

   def slots_saves_memory():
       slotted, plain = Pixel(1, 2, 3), _PlainPixel(1, 2, 3)
       return (not hasattr(slotted, "__dict__")
               and sys.getsizeof(slotted) < sys.getsizeof(plain) + sys.getsizeof(plain.__dict__))
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Leaving out `@functools.wraps`, so the wrapped function is named `wrapper` and task 1 fails.
- Forgetting `nonlocal calls`, which gives `UnboundLocalError` on the first call.
- Returning a list from `error_lines` (square brackets); the check requires a generator.
