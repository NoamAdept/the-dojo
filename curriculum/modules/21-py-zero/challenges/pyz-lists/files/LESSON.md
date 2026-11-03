# Lists: lesson

A **list** is a group of values in a fixed order. You write it in square brackets:

```python
snrs = [12, 3, 18, 7]
names = ["alpha", "bravo"]
empty = []
```

It is like a C++ `std::vector`. It can grow and shrink, and it knows its own length.

**Indexing.** Each item has a position number, called its **index**. The index starts at 0 (the same as in C++):

```python
snrs[0]      # 12, the first item
snrs[3]      # 7
snrs[-1]     # 7, negative counts from the end: -1 is the last
snrs[-2]     # 18
len(snrs)    # 4, how many items
snrs[1] = 5  # change an item: now [12, 5, 18, 7]
```

Sometimes you ask for an index that does not exist, like `snrs[10]`. Then Python gives an `IndexError`.
This is better than C++. In C++, `v[10]` on a `std::vector` can quietly give you random garbage.

**Slicing** takes a part of a list as a new list: `items[start:stop]`. The `stop` item is not included
(the same as in `range`). You can leave out one side. No start means "from the beginning". No stop means
"to the end":

```python
snrs[1:3]    # [3, 18]
snrs[:2]     # [12, 3]   the first two
snrs[2:]     # [18, 7]   from index 2 to the end
snrs[1:-1]   # [3, 18]   everything except the first and last
```

**Growing.** `items.append(x)` adds `x` to the end. Some functions belong to a value, and you call them with
a dot like this. Such a function is called a **method**:

```python
found = []
found.append(4)
found.append(9)      # found is now [4, 9]
```

**Looping over items.** `for` works directly on a list. It gives you each item. You do not need an index:

```python
total = 0
for s in snrs:
    total += s
```

Some useful built-in functions:

- `sum(items)`, `max(items)` and `min(items)`.
- `sorted(items)`: a sorted copy.
- `x in items`: True if `x` is in the list.

**List comprehensions.** A list comprehension builds a list from a loop in one line. These two do the same thing:

```python
doubled = []
for s in snrs:
    doubled.append(s * 2)

doubled = [s * 2 for s in snrs]
```

Read it as "`s * 2`, for each `s` in `snrs`". You can add a filter: `[s for s in snrs if s > 5]`. You will
see this a lot in real Python. For example, `[int(x) for x in words]` turns a list of strings into ints.

**New words**
- list: a group of values in order that can grow, written `[a, b, c]`.
- index: an item's position, counting from 0. `-1` is the last item.
- slice: `items[start:stop]`, a new list with part of the items (the stop item is not included).
- method: a function that belongs to a value. You call it with a dot, like `items.append(x)`.
- len: the built-in function that gives the number of items.
- list comprehension: `[expression for x in items]`. It builds a list in one line.

## Offline help

- Offline: `python3 -m pydoc list`
