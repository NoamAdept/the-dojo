# Functions: def and return

`pyz-functions` · Blue Belt

**Goal:** Replace each `raise NotImplementedError` in `tasks.py` with a one-line body that returns the right value, and change `average` from `print` to `return`.

**File `tasks.py`**

```python
"""Python from Zero 03: functions."""

def double(n):
    return n * 2

def greet(name):
    return f"Hello, {name}!"

def area(width, height):
    return width * height

def to_khz(hz):
    return hz / 1000

def average(a, b):
    return (a + b) / 2

def quadruple(n):
    return double(double(n))
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
