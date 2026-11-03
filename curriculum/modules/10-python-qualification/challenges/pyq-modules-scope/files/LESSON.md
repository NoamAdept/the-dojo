# Modules, Packages and Namespaces: lesson

### 1. What is a Module?

In Python, a **module** is just a file with Python definitions and statements in it. The file name is the module name plus `.py` at the end. Modules help you organize your code in a sensible way. When you put related code together in a module, the code is easier to understand and to use.

```python
import math

# Using the imported module module
# This is similar to #include <cmath> and using std::
print(f"The value of pi is: {math.pi}")
print(f"Square root of 16 is: {math.sqrt(16)}")

# Attributes of the module object itself
print(f"Module name: {math.__name__}")
print(f"Module documentation: {math.__doc__[:50]}...")
```

### 2. Import Variants (`import` vs `from`)

You can import a module in different ways. This is like `using namespace` or a single `using` declaration in C++.

- `import X`: imports the module X. You must write `X.name` each time you use a name from it.
- `from X import Y`: imports only the name Y from module X. You can then write `Y` directly.
- `from X import *`: imports all names. **Do not do this.** It fills your namespace (your set of names) with names you did not choose.

```python
from datetime import date
import random

# direct usage
today = date.today()
print(f"Today's date: {today}")

# prefixed usage
rand_num = random.randint(1, 10)
print(f"Random number: {rand_num}")
```

### 3. Aliasing with `as`

Use `as` to give a module or an imported object a second, shorter name (an alias). Many people do this with popular libraries, for example `import numpy as np`.

```python
import math as m
from datetime import datetime as dt

print(f"Cosine of 0: {m.cos(0)}")
print(f"Current time: {dt.now()}")
```

### 4. Packages and `__init__.py`

A **package** is a folder of modules. You reach the modules with "dotted module names", such as `sound.formats`. The folder must contain a file named `__init__.py` (it can be empty). Then Python treats the folder as a package.

Structure:
```
sound/
    __init__.py
    formats/
        __init__.py
        wavread.py
```
Usage: `import sound.formats.wavread`

```python
# Emulating a package structure for demonstration
import os

os.makedirs("mypkg", exist_ok=True)
with open("mypkg/__init__.py", "w") as f:
    f.write("print('Initializing mypkg...')\npackage_var = 'Hello from Init'")

with open("mypkg/submod.py", "w") as f:
    f.write("def greet(): return 'Greetings from submodule!'")

import mypkg.submod
print(mypkg.package_var)
print(mypkg.submod.greet())
```

### 5. Scope Resolution (LEGB Rule)

Scope resolution is the order in which Python searches for a variable name. It follows the **LEGB** rule:

1. **L**ocal (inside the current function)
2. **E**nclosing (inside any outer function around it)
3. **G**lobal (at module level)
4. **B**uilt-in (names that Python gives you, such as `len`)

```python
x = "Global X"

def outer():
    x = "Enclosing X"
    def inner():
        x = "Local X"
        print(x) # L
    inner()
    print(x) # E

outer()
print(x) # G
```

### 6. Modifying Scopes: `global` and `nonlocal`

Do you want to assign to a global variable inside a function? Then you must declare it `global` first. For a variable in an outer function (in nested functions), use `nonlocal`.

```python
counter = 0

def update_globals():
    global counter
    counter += 1

update_globals()
print(f"Global Counter: {counter}")

def outer_func():
    x = 0
    def inner_func():
        nonlocal x
        x = 10
    inner_func()
    print(f"Modified Enclosing x: {x}")

outer_func()
```

### 7. The `dir()` Function

The built-in function `dir()` shows which names a module defines. It returns a sorted list of strings.

```python
import sys

# List names in the sys module
names = dir(sys)
print(f"First 5 names in sys: {names[:5]}")

# List names in current scope
current_names = dir()
print(f"Current scope names: {current_names[-5:]}")
```

### 8. `__name__ == "__main__"`

This check lets a file work in 2 ways. You can run it as a script on its own, or import it as a module. If you run the file directly, `__name__` is `"__main__"`. If you import it, `__name__` is the module's name.

```python
if __name__ == "__main__":
    print("This code is running because this notebook is the 'main' program.")
else:
    print("This code would run if this notebook was imported.")
```

---

## New words

- **module**: 1 Python file that you can import.
- **package**: a folder of modules with an `__init__.py` file.
- **namespace**: a set of names, kept apart from other sets of names.
- **alias**: a second name for the same thing, made with `as`.
- **scope**: the part of the code where a name is visible.
- **closure**: an inner function that keeps the variables of its outer function.
- **decorator**: a function that takes a function and returns a function. You write it as `@name` above a `def`.

## Offline help

- Offline: `python3 -m pydoc import`
