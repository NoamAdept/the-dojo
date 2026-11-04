# Loops: for, range and while

`pyz-loops` · Blue Belt

**Goal:** Write six functions in `tasks.py` that use `for` loops over `range` and `while` loops to add, multiply, count and build text.

**File `tasks.py`**

```python
"""Python from Zero 05: loops."""

def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def countdown(n):
    text = ""
    for i in range(n, 0, -1):
        text += f"{i} "
    return text + "liftoff"

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def count_multiples(n, k):
    count = 0
    for i in range(1, n + 1):
        if i % k == 0:
            count += 1
    return count

def count_digits(n):
    digits = 1
    while n >= 10:
        n = n // 10
        digits += 1
    return digits

def first_power_over(limit):
    power = 1
    while power <= limit:
        power *= 2
    return power
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
