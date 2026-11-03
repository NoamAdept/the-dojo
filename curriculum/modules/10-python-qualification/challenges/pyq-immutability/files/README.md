# Immutability and State



## Module 4: Immutability and State

In C++, `const` is a core part of the language, and the compiler enforces it. In Python, immutability belongs to the *object type*, not to the variable. You need to know which types are mutable (can change) and which are immutable (cannot change). This helps you write correct Python code without bugs.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Tuple access**: `try_modify_tuple()` tries to set index 1 of `(100, 200, 300)` to 250. It catches the error. It returns the type of the exception it caught.
2. **Unpacking**: `split_head(data)` returns `(head, tail)`. Use star unpacking. `tail` must be a list.
3. **NamedTuple**: define `Server(NamedTuple)` with `address: str` and `active: bool`.
4. **Dictionary key**: `frozenset_key()` does 2 things:
   - It shows that a set cannot be a dict key (catch the `TypeError`).
   - It then returns a dict with `frozenset({1, 2})` as the key and `"ok"` as the value.
5. **Unique filter**: `unique_elements(lst)` returns a sorted tuple of the unique integers (each integer only once).
6. **Immutable point**: `ImmutablePoint(x, y)` uses `__slots__` and read-only properties. After `__init__`, setting `x`, `y` or any new attribute raises `AttributeError`.
7. **Memoize decorator**: `memoize` saves results in a dict (a cache). The key is the arguments.
   - Convert list arguments to tuples (recursively, so lists inside lists too). Then they can be cache keys.
   - Make the cache available as `wrapper.cache`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
