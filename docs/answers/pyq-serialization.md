## Dataclasses and Serialization

*pyq-serialization · medium*

**Goal.** Define dataclasses (one frozen), save and load data with `json` and `pickle`, and build a `file_cache` decorator that keeps results in a pickle file between runs.

**You need to know.**

- `@dataclass` and `@dataclass(frozen=True)`.
- `json.dumps` / `json.dump` / `json.load` (text) vs `pickle.dumps` / `pickle.load` (bytes).
- `dataclasses.asdict` and rebuilding with `User(**row)`.
- Files for pickle must be opened in binary mode (`"rb"`, `"wb"`).

**Walkthrough.**

1. Run `./check` to see the failures. The imports you need are already at the top of `tasks.py`.

   ```bash
   ./check
   ```

2. Task 1. Replace the comment with the dataclass.

   ```python
   @dataclass
   class Item:
       name: str
       price: float
   ```

3. Task 2. `json.dumps` returns a string.

   ```python
   def student_json():
       return json.dumps({"name": "John", "grades": [80, 90]})
   ```

4. Task 3. `dumps` gives bytes, `loads` rebuilds the object.

   ```python
   def pickle_roundtrip(obj):
       data = pickle.dumps(obj)
       return data, pickle.loads(data)
   ```

5. Task 4. `frozen=True` makes any assignment raise `FrozenInstanceError`.

   ```python
   @dataclass(frozen=True)
   class Settings:
       debug: bool
   ```

6. Task 5. Plain JSON write and read with `with open`.

   ```python
   def save_config(config, filename):
       with open(filename, "w") as fh:
           json.dump(config, fh, indent=2)

   def load_config(filename):
       with open(filename) as fh:
           return json.load(fh)
   ```

7. Task 6. `asdict` turns each user into a dict JSON can write; `User(**row)` turns each dict back into a `User`.

   ```python
   @dataclass
   class User:
       name: str
       age: int

   def serialize_users(users, filename):
       with open(filename, "w") as fh:
           json.dump([asdict(u) for u in users], fh)

   def deserialize_users(filename):
       with open(filename) as fh:
           return [User(**row) for row in json.load(fh)]
   ```

8. Task 7. A decorator with an argument, so three levels. The file is read inside `wrapper` on every call, which is how a brand new wrapper (the check makes a second one) still sees earlier results. Only call `func` and rewrite the file on a cache miss.

   ```python
   def file_cache(filename):
       def decorator(func):
           @functools.wraps(func)
           def wrapper(x):
               cache = {}
               if os.path.exists(filename):
                   with open(filename, "rb") as fh:
                       cache = pickle.load(fh)
               if x not in cache:
                   cache[x] = func(x)
                   with open(filename, "wb") as fh:
                       pickle.dump(cache, fh)
               return cache[x]
           return wrapper
       return decorator
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Reading the pickle file once when decorating (outside `wrapper`); the second wrapper then misses results written by the first.
- Opening the pickle file in text mode (`"w"` / `"r"`), which raises `TypeError` or a decode error.
- Returning `json.dump(...)` from `student_json`; `dump` writes to a file and returns `None`, use `dumps`.
