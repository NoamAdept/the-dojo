## Resource Management and Context Managers

*pyq-context-managers · medium*

**Goal.** Write context managers in both styles (generator with `@contextmanager`, and classes with `__enter__` / `__exit__`), plus a timing decorator, in `tasks.py`.

**You need to know.**

- `with open(...)` closes the file for you.
- `@contextmanager`: code before `yield` is enter, code after is exit; wrap `yield` in `try`/`finally`.
- `__exit__(self, exc_type, exc, tb)`: returning `True` swallows the exception, `False` lets it propagate.
- `tempfile.TemporaryDirectory()` and `time.perf_counter()`.
- `global` for changing a module-level variable.

**Walkthrough.**

1. Run `./check` to see the failures. Add `import functools` and `import os` at the top of `tasks.py`; the solution uses both.

   ```bash
   ./check
   ```

2. Task 1. Write one number per line.

   ```python
   def write_numbers(path):
       with open(path, "w") as fh:
           for i in range(1, 11):
               fh.write(f"{i}\n")
   ```

3. Task 2. `finally` makes the closing tag print even if the body raises. Replace the starter's `raise NotImplementedError` and `yield` with this.

   ```python
   @contextmanager
   def html_tag(name):
       print(f"<{name}>")
       try:
           yield
       finally:
           print(f"</{name}>")
   ```

4. Task 3. `exc_type` is not `None` only when the body raised. Returning `False` re-raises it.

   ```python
   class ExceptionSpy:
       def __init__(self):
           self.seen = False
       def __enter__(self):
           return self
       def __exit__(self, exc_type, exc, tb):
           if exc_type is not None:
               self.seen = True
               print("An error occurred!")
           return False
   ```

5. Task 4. The directory exists inside the `with` and is deleted when it ends.

   ```python
   def temp_dir_lifecycle():
       with tempfile.TemporaryDirectory() as path:
           inside = os.path.isdir(path)
       return inside, os.path.exists(path)
   ```

6. Task 5. `Timer` records the start on enter and stores `elapsed` on exit. `time_it` runs the call inside a `Timer` and saves the time on the wrapper.

   ```python
   class Timer:
       def __enter__(self):
           self.start = time.perf_counter()
           return self
       def __exit__(self, *exc):
           self.elapsed = time.perf_counter() - self.start
           return False

   def time_it(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           with Timer() as t:
               result = func(*args, **kwargs)
           wrapper.last_elapsed = t.elapsed
           return result
       return wrapper
   ```

7. Task 6. Add `__enter__` and `__exit__` to the starter's `DatabaseConnection`. Enter returns a `Cursor`, not `self`.

   ```python
   def __enter__(self):
       self.log.append("connect")
       return Cursor()

   def __exit__(self, exc_type, exc, tb):
       self.log.append("rollback" if exc_type else "commit")
       self.log.append("disconnect")
       return False
   ```

8. Task 7. Both methods change the module-level `LEVEL`, so both need `global LEVEL`.

   ```python
   class Indenter:
       def __enter__(self):
           global LEVEL
           LEVEL += 1
           return self
       def __exit__(self, *exc):
           global LEVEL
           LEVEL -= 1
           return False

   def indented(msg):
       return "    " * LEVEL + msg
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- In `html_tag`, a plain `yield` without `try`/`finally`; the closing tag never prints when the body raises.
- Returning `True` from `__exit__` in `ExceptionSpy` or `DatabaseConnection`, which hides the error; the check expects it to propagate.
- Forgetting `global LEVEL` in `Indenter`, which gives `UnboundLocalError`.
