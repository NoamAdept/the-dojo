# Modules, Packages and Namespaces



## Module 1: Modules, Packages, and Namespaces

Welcome to Module 1 of the Python Qualification! In this part, you learn how Python organizes code. You also learn how it keeps track of names (identifiers). Do you know C++? Then think of a module as a translation unit and a namespace together, but easier to use.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Edit `tasks.py`. Each stub (an empty starting function) says what to return. You also create 1 small package.

1. **Basic math import**: `factorial_of_ten()` uses the `math` module. It returns 10! (10 factorial).
2. **Custom alias**: `current_dir()` imports `os` as `operating_system`. It returns `operating_system.getcwd()`.
3. **Scope fix**: make `increment()` add 1 to the module-level `score`. Use the `global` keyword.
4. **Inner functions**: `maker(n)` returns an inner function. The inner function adds `n` to its argument.
5. **Calculator module**: create `simple_calc.py` with `add(a, b)` and `sub(a, b)`. Then `calc_demo()` imports it and returns `(add(2, 3), sub(10, 4))`.
6. **Config package**: create these 2 files:
   - `config_pkg/settings.py` defines a dict `DEFAULT_CONFIG`. It needs at least a `"sample_rate"` key.
   - `config_pkg/__init__.py` re-exports it (imports it so others can import it from the package).

   After that, `from config_pkg import DEFAULT_CONFIG` must work.
7. **Registry decorator**: `register` adds the decorated function to the global dict `REGISTRY`. The key is the function's name. `register` returns the function unchanged. Decorate 3 functions. Then make `run_all()` call every registered function. It returns a dict from name to result.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
