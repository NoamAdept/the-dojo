# Performance and Decorators

`pyq-performance` · Blue Belt

**Goal:** Write decorators (a logger and a call limiter), generators for lazy processing, a `timeit` comparison, and `__slots__` classes that save memory, all in `tasks.py`.

**File `tasks.py`**

```python
"""Python Qualification 13: performance and decorators."""
import functools
import sys
import timeit

def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def squares(n):
    for i in range(n + 1):
        yield i * i

def compare_join(number=100_000):
    join = timeit.timeit('" ".join(["a", "b", "c"])', number=number)
    concat = timeit.timeit('"a" + " " + "b" + " " + "c"', number=number)
    return join, concat

class Point:
    __slots__ = ("x", "y")

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

def read_large_file(path):
    with open(path) as fh:
        for line in fh:
            yield line.rstrip("\n")

def error_lines(path):
    return (line for line in read_large_file(path) if "ERROR" in line)

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

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
