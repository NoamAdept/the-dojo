# Modules, Packages and Namespaces

`pyq-modules-scope` · Blue Belt

**Goal:** Finish the stubs in `tasks.py`, create a module `simple_calc.py` and a package `config_pkg/`, and build a small decorator registry.

**File `config_pkg/__init__.py`**

```python
from .settings import DEFAULT_CONFIG
```

**File `config_pkg/settings.py`**

```python
DEFAULT_CONFIG = {"sample_rate": 2_048_000, "gain": 20}
```

**File `simple_calc.py`**

```python
def add(a, b):
    return a + b

def sub(a, b):
    return a - b
```

**File `tasks.py`**

```python
"""Python Qualification 01: modules, packages and namespaces."""

score = 0
REGISTRY = {}

def factorial_of_ten():
    import math
    return math.factorial(10)

def current_dir():
    import os as operating_system
    return operating_system.getcwd()

def increment():
    global score
    score += 1

def maker(n):
    def inner(x):
        return x + n
    return inner

def calc_demo():
    from simple_calc import add, sub
    return add(2, 3), sub(10, 4)

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

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
