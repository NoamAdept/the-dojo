# Loops: for, range and while: lesson

**for and range.** In C++ you counted with `for (int i = 0; i < 5; i++)`. In Python you write:

```python
for i in range(5):
    print(i)
```

This prints `0 1 2 3 4`, one number on each line. `range(5)` gives the numbers from 0 up to 5, but **not
including** 5. The loop gives each number to `i`, one after the other. It runs the indented body once for
each number. Here are other forms:

```python
range(1, 6)        # 1 2 3 4 5      (start, stop)
range(0, 10, 2)    # 0 2 4 6 8      (start, stop, step)
range(5, 0, -1)    # 5 4 3 2 1      (counting down)
```

The stop number is never included. So "1 to n" is `range(1, n + 1)`.

**Accumulating.** To add up many values, set a variable to 0 before the loop. Then add to it inside the loop:

```python
def sum_odds(n):
    total = 0
    for i in range(1, n + 1, 2):
        total += i         # same as total = total + i
    return total
```

Python has `+=`, `-=`, `*=` and `//=`, like C++. But it has **no** `++` or `--`. Write `i += 1` instead.
Look at the `return`: it is *not* indented under the `for`. So it runs once, after the loop has finished.
You can make a string grow in the same way. Start with `""` and do `text += "more"`.

**while.** `while condition:` repeats its body while the condition is True. Use it when you do not know
before the loop how many times it must run:

```python
def halvings(n):
    count = 0
    while n > 1:
        n = n // 2
        count += 1
    return count
```

Something in the body must change the condition. If not, the loop never ends. (Press Ctrl-C to stop a
program that is stuck.) `break` leaves a loop early, as in C++.

**Loops plus if.** You can put an `if` inside a loop body, indented one more level. Then the loop acts only
on some values.

**New words**
- loop: code that runs its body again and again.
- for: a loop that runs once for each item, such as each number from `range`.
- range(start, stop, step): the numbers from start up to stop (stop is not included).
- accumulator: a variable that collects a result during a loop, like a running total.
- while: a loop that runs while a condition stays True.
- `+=`: add to a variable in place (`x += 1`). Python has no `++`.

## Offline help

- Offline: `python3 -m pydoc for`, `python3 -m pydoc while`, `python3 -m pydoc range`
