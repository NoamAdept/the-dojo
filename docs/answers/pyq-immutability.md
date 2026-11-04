# Immutability and State

`pyq-immutability` · Blue Belt

**Goal:** Show tuple and set immutability rules in code, define a `NamedTuple`, build a read-only `ImmutablePoint`, and write a `memoize` decorator that can cache calls with list arguments.

**File `tasks.py`**

```python
"""Python Qualification 04: immutability and state."""
from typing import NamedTuple

def try_modify_tuple():
    t = (100, 200, 300)
    try:
        t[1] = 250
    except TypeError as exc:
        print(f"Cannot modify a tuple: {exc}")
        return type(exc)

def split_head(data):
    head, *tail = data
    return head, tail

class Server(NamedTuple):
    address: str
    active: bool

def frozenset_key():
    try:
        {{1, 2}: "nope"}
    except TypeError as exc:
        print(f"set is unhashable: {exc}")
    return {frozenset({1, 2}): "ok"}

def unique_elements(lst):
    return tuple(sorted(set(lst)))

class ImmutablePoint:
    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        object.__setattr__(self, "_x", x)
        object.__setattr__(self, "_y", y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __setattr__(self, name, value):
        raise AttributeError(f"ImmutablePoint is read-only ({name})")

def _freeze(value):
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    if isinstance(value, dict):
        return tuple(sorted((k, _freeze(v)) for k, v in value.items()))
    if isinstance(value, set):
        return frozenset(_freeze(v) for v in value)
    return value

def memoize(func):
    cache = {}

    def wrapper(*args, **kwargs):
        key = (_freeze(args), _freeze(kwargs))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache
    return wrapper
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
