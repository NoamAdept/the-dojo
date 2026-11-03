## Modules, Packages and Namespaces

*pyq-modules-scope · easy*

**Goal.** Finish the stubs in `tasks.py`, create a module `simple_calc.py` and a package `config_pkg/`, and build a small decorator registry.

**You need to know.**

- `import x`, `import x as y`, `from x import y` and relative imports (`from .settings import ...`).
- The LEGB scope rule and the `global` keyword.
- Closures (an inner function remembers variables of the outer one).
- A package is a folder with `__init__.py`.
- Decorators run when the function is defined.

**Walkthrough.**

1. Run `./check` to see what fails.

   ```bash
   ./check
   ```

2. Task 1. `math.factorial` does the work.

   ```python
   def factorial_of_ten():
       import math
       return math.factorial(10)
   ```

3. Task 2. The check also greps `tasks.py` for the text `operating_system`, so the alias must really be used.

   ```python
   def current_dir():
       import os as operating_system
       return operating_system.getcwd()
   ```

4. Task 3. Without `global`, the assignment in `score += 1` makes `score` local and raises `UnboundLocalError`.

   ```python
   def increment():
       global score
       score += 1
   ```

5. Task 4. `inner` uses `n` from the enclosing call, which creates a closure (the check looks at `__closure__`).

   ```python
   def maker(n):
       def inner(x):
           return x + n
       return inner
   ```

6. Task 5. Create `simple_calc.py` next to `tasks.py`, then import from it.

   ```python
   # simple_calc.py
   def add(a, b):
       return a + b

   def sub(a, b):
       return a - b
   ```

   ```python
   # tasks.py
   def calc_demo():
       from simple_calc import add, sub
       return add(2, 3), sub(10, 4)
   ```

7. Task 6. Make the folder and two files. The `__init__.py` re-exports the same dict object, so `config_pkg.DEFAULT_CONFIG is config_pkg.settings.DEFAULT_CONFIG`.

   ```bash
   mkdir config_pkg
   echo 'DEFAULT_CONFIG = {"sample_rate": 2_048_000, "gain": 20}' > config_pkg/settings.py
   echo 'from .settings import DEFAULT_CONFIG' > config_pkg/__init__.py
   ```

8. Task 7. `register` stores the function under its name and returns it unchanged. Decorating three functions fills the registry at import time; `run_all` calls each one.

   ```python
   def register(func):
       REGISTRY[func.__name__] = func
       return func

   @register
   def hello():
       return "hello"

   @register
   def answer():
       return 42

   @register
   def pi_ish():
       return 3.14

   def run_all():
       return {name: func() for name, func in REGISTRY.items()}
   ```

   The three decorated functions must be defined after `register` in the file, or the decorator name does not exist yet.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Putting `simple_calc.py` or `config_pkg/` somewhere other than the folder that holds `tasks.py`; the check imports them from the current directory.
- Writing `from settings import DEFAULT_CONFIG` (no dot) in `__init__.py`, which fails with `ModuleNotFoundError`.
- Returning `None` from `register` (forgetting `return func`), which replaces each decorated function with `None`.
