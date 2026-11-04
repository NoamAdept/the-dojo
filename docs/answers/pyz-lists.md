# Lists

`pyz-lists` · Blue Belt

**Goal:** Write six functions in `tasks.py` that index, slice, build and summarise lists, without changing the list they are given.

**File `tasks.py`**

```python
"""Python from Zero 06: lists."""

def ends(items):
    return [items[0], items[-1]]

def middle(items):
    return items[1:-1]

def evens_up_to(n):
    result = []
    for i in range(0, n + 1, 2):
        result.append(i)
    return result

def count_above(items, limit):
    count = 0
    for x in items:
        if x > limit:
            count += 1
    return count

def average(items):
    return sum(items) / len(items)

def squares(n):
    return [i * i for i in range(n)]
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
