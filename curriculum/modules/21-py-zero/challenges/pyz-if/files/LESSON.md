# Decisions: if, elif, else: lesson

**Comparisons** test two values. They give back a bool (`True` or `False`):

| write | means |
|---|---|
| `a == b` | a equals b. Use two `=` here. One `=` stores a value. |
| `a != b` | a is not equal to b |
| `a < b`, `a > b` | less than, greater than |
| `a <= b`, `a >= b` | less or equal, greater or equal |

```console
>>> 5 > 3
True
>>> 10 % 2 == 0
True
```

**Combining.** C++ has `&&`, `||` and `!`. Python uses the words `and`, `or` and `not` instead:

```python
has_antenna and has_power      # True only if both are True
rainy or windy                 # True if at least one is True
not is_on                      # flips True and False
```

In Python you can also chain comparisons, as you do in maths. `30 <= f < 300` means
`30 <= f and f < 300`.

**if / elif / else.** This is like `if (...) { } else if (...) { } else { }` in C++. But Python uses colons and indentation.
You do not need brackets around the condition:

```python
def describe(temp):
    if temp < 0:
        return "freezing"
    elif temp < 20:
        return "cool"
    else:
        return "warm"
```

Python checks the conditions from top to bottom. It runs only the **first** block where the condition is True.

- `elif` (short for "else if") can appear as many times as you like.
- `else` runs for every case that is left. You do not have to use `else`.

The order matters. When we reach `elif temp < 20`, we already know that `temp >= 0`.

**Boundaries.** Most bugs (mistakes in code) are at the edges. A boundary is the exact value where the answer changes.
If a rule says "under 30 is HF", then 29.9 is HF and 30 is not.
Always try the exact edge values at the prompt: `describe(0)`, `describe(20)`.

**New words**
- comparison: a test such as `a < b` that gives True or False.
- condition: the comparison (or bool) that an `if` tests.
- if / elif / else: run the first block where the condition is True. else runs when no condition was True.
- and / or / not: combine or flip bool values (like `&&`, `||`, `!` in C++).
- boundary: the exact value where a rule changes from one answer to the next.
- bug: a mistake in code.

## Offline help

- Offline: `python3 -m pydoc if` and `python3 -m pydoc COMPARISON`
