# Performance and Decorators: lesson

### 1. Decorators 101

A decorator is a function that takes another function and adds new behavior to it. You do not change the code of the original function. People often use decorators for:

- logging
- access control (who may call the function)
- instrumentation (measuring what the code does)

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

### 2. Using `functools.wraps`

When you wrap a function, you lose its metadata (`__name__`, `__doc__`). Metadata is information about the function, like its name and help text. Use `@functools.wraps` to keep it.

```python
import functools

def better_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Wrapped call")
        return func(*args, **kwargs)
    return wrapper

@better_decorator
def add(x, y):
    """Adds two numbers."""
    return x + y

print(f"Name: {add.__name__}")
print(f"Doc: {add.__doc__}")
```

### 3. Decorators with Arguments

For a decorator that takes arguments, you need 3 levels of functions, one inside the other:

- The outer layer takes the arguments.
- The middle layer takes the function.
- The inner layer is the wrapper.

```python
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

greet("World")
```

### 4. Generators and Lazy Evaluation

A generator calculates each value only when you ask for it (`yield`). It does not store all the values in memory. This is called lazy evaluation. It is very important when you process large amounts of data.

```python
import sys

def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

gen = infinite_sequence()
print(next(gen))
print(next(gen))

# Size comparison
huge_list = [i for i in range(100000)]
huge_gen = (i for i in range(100000))

print(f"List Bytes: {sys.getsizeof(huge_list)}")
print(f"Gen Bytes:  {sys.getsizeof(huge_gen)}")
```

### 5. Benchmarking with `timeit`

Do not guess how fast code is. Measure it. `timeit` runs a small piece of code many times. This gives an average, so random delays (noise) matter less.

```python
import timeit

code_list = "res = []\nfor i in range(1000): res.append(i)"
code_comp = "res = [i for i in range(1000)]"

time_list = timeit.timeit(code_list, number=1000)
time_comp = timeit.timeit(code_comp, number=1000)

print(f"Loop: {time_list:.5f}s")
print(f"Comp: {time_comp:.5f}s (usually faster)")
```

### 6. Profiling with `cProfile`

For a full application, use `cProfile`. A profiler shows exactly which functions use the most time.

```python
import cProfile
import re

def slow_regex():
    for _ in range(10000):
        re.search(r"[a-z]+", "hello world")

cProfile.run("slow_regex()")
```

### 7. `__slots__` Optimization

Normal Python objects store their attributes in a `__dict__`. This uses a lot of memory. `__slots__` tells Python the exact list of attributes. This saves memory and makes attribute access faster. You also cannot add new attributes.

```python
class SlotFree:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Slotted:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = Slotted(1, 2)
try:
    obj.z = 3 # AttributeError
except AttributeError as e:
    print(f"Cannot add attributes: {e}")
```

### 8. Caching (`functools.lru_cache`)

Memoization means: save the result of a function call, and reuse it the next time you get the same input. It can make slow recursive functions (functions that call themselves) much faster. `functools.lru_cache` does this for you.

```python
import time

@functools.lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

start = time.time()
print(f"Fib(35): {fib(35)}")
print(f"Time: {time.time() - start:.4f}s")
```

---

## New words

- **decorator**: a function that wraps another function to add behavior.
- **wrapper**: the inner function that a decorator returns.
- **metadata**: information about a function, like `__name__` and `__doc__`.
- **generator**: a function with `yield`. It makes values one at a time.
- **lazy evaluation**: calculating a value only when you need it.
- **benchmark**: a measurement of how fast code runs.
- **profiler**: a tool that shows where a program spends its time.
- **memoization**: saving results so you do not calculate them again.
