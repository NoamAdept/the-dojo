## Immutability and State

*pyq-immutability · medium*

**Goal.** Show tuple and set immutability rules in code, define a `NamedTuple`, build a read-only `ImmutablePoint`, and write a `memoize` decorator that can cache calls with list arguments.

**You need to know.**

- Tuples are immutable; assigning to an index raises `TypeError`.
- Star unpacking `head, *tail = data`.
- `typing.NamedTuple` with annotated fields.
- Only hashable values can be dict keys: `frozenset` yes, `set` and `list` no.
- `__slots__`, `@property` and overriding `__setattr__`.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1. Catch the `TypeError` and return its type (the class, not the instance).

   ```python
   def try_modify_tuple():
       t = (100, 200, 300)
       try:
           t[1] = 250
       except TypeError as exc:
           return type(exc)
   ```

3. Task 2. The starred name always collects a list, even when it is empty.

   ```python
   def split_head(data):
       head, *tail = data
       return head, tail
   ```

4. Task 3. Replace the comment in the starter with the class. The annotations become the fields.

   ```python
   class Server(NamedTuple):
       address: str
       active: bool
   ```

5. Task 4. Using a set as a key raises `TypeError` because a set is unhashable; a `frozenset` is hashable.

   ```python
   def frozenset_key():
       try:
           {{1, 2}: "nope"}
       except TypeError as exc:
           print(f"set is unhashable: {exc}")
       return {frozenset({1, 2}): "ok"}
   ```

6. Task 5. `set` drops duplicates, `sorted` orders them, `tuple` makes the result immutable.

   ```python
   def unique_elements(lst):
       return tuple(sorted(set(lst)))
   ```

7. Task 6. `__setattr__` always raises, so `__init__` must bypass it with `object.__setattr__`. `__slots__` stops a `__dict__` from existing, and the properties have no setter, so `x` and `y` are read-only.

   ```python
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
   ```

8. Task 7. A list cannot be a dict key, so `_freeze` turns lists into tuples (recursively) and dicts such as `kwargs` into sorted tuples of pairs. The key is `(frozen args, frozen kwargs)`.

   ```python
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

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Returning the exception instance (`exc`) in task 1 instead of `type(exc)`; the check uses `is TypeError`.
- Setting `self._x = x` in `__init__` of `ImmutablePoint`, which hits the overridden `__setattr__` and raises.
- Ignoring `kwargs` in the memoize key, so `total([1,2,3], scale=2)` returns the cached 6 instead of 12.
