# Project Structure and Packaging: lesson

### 1. Virtual Environments (`venv`)

Never install packages globally (for the whole system). Always use a Virtual Environment. A virtual environment is a private folder with its own Python and its own packages. It keeps the dependencies (the packages your project needs) of each project apart.

Use these commands to create and turn on a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

```python
import sys

# Check if we are in a virtual environment
def in_venv():
    return sys.prefix != sys.base_prefix

print(f"Running in venv? {in_venv()}")
print(f"Python Executable: {sys.executable}")
```

### 2. Standard Project Layout

Most projects use a standard folder layout. A typical "Src-Layout" puts the real code inside a `src/` folder. It looks like this:

```
my_project/
├── pyproject.toml       # Build system & dependencies
├── README.md
├── src/
│   └── my_package/      # Actual code
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

```python
import os

# Simulating creating this structure
os.makedirs("demo_project/src/demo_pkg", exist_ok=True)
os.makedirs("demo_project/tests", exist_ok=True)

print("Created demo_project structure.")
```

### 3. `pyproject.toml`: The Modern Config

`pyproject.toml` replaces the older `setup.py` and `requirements.txt` files. TOML is a simple text format for settings. The file says:

- what the build system needs
- the settings for tools (black, isort, mypy)

```python
toml_content = """
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "demo_pkg"
version = "0.1.0"
dependencies = [
    "requests",
    "numpy"
]
"""

with open("demo_project/pyproject.toml", "w") as f:
    f.write(toml_content)

print("Written pyproject.toml")
```

### 4. `__main__.py`: Executable Packages

If you add a `__main__.py` file to your package, you can run the package with `python -m my_package`.

```python
main_code = """
import sys

def main():
    print(f"Running demo_pkg with args: {sys.argv}")

if __name__ == '__main__':
    main()
"""

with open("demo_project/src/demo_pkg/__main__.py", "w") as f:
    f.write(main_code)
```

### 5. Relative Imports

Inside your package, use relative imports. A relative import finds a module by its position next to the current module. A sibling is a module in the same folder. A parent is the folder one level up.

- `from . import module` (Sibling)
- `from .. import subpkg` (Parent)

```python
# Just creating a dummy sibling file
with open("demo_project/src/demo_pkg/utils.py", "w") as f:
    f.write("def helper(): return 'Help'")

# Creating __init__ that uses relative import
init_code = """
from .utils import helper

print(f"Loaded: {helper()}")
"""

with open("demo_project/src/demo_pkg/__init__.py", "w") as f:
    f.write(init_code)
```

### 6. Testing Structure (`pytest`)

Put your tests in the `tests/` folder. Python has `unittest` built in. But most companies use `pytest` (it is the industry standard). It is simple, and it has strong fixtures. A fixture is setup code that many tests can share.

```python
test_code = """
import pytest
from demo_pkg.utils import helper

def test_helper():
    assert helper() == "Help"
"""

with open("demo_project/tests/test_basic.py", "w") as f:
    f.write(test_code)
```

### 7. Linters and Formatters

Professional projects make all code follow one style. A linter is a tool that finds style problems and likely bugs. A formatter is a tool that changes the layout of your code for you.

- **Black**: Code formatter (it applies the PEP8 style automatically).
- **Isort**: Sorts imports.
- **MyPy**: Static type checker (it finds type errors without running the code).
- **Ruff**: A new linter. It is written in Rust and is very fast.

```python
# Config for black in pyproject.toml
black_config = """

[tool.black]
line-length = 88
target-version = ['py310']
"""

with open("demo_project/pyproject.toml", "a") as f:
    f.write(black_config)
```

### 8. Importing from `src` (The Development Pain)

This is a common problem during development. With the `src/` layout, you cannot simply `import demo_pkg` from the root directory of the project. First you must install the package in editable mode: `pip install -e .`. Editable mode means Python uses your source files directly, so your changes show up at once.

The example below uses a hack (a quick trick) instead of pip:

```python
import sys
import os

# Hack to simulate 'pip install -e .'
sys.path.append(os.path.abspath("demo_project/src"))

# Now we can import it
import demo_pkg
print(f"Package imported from: {demo_pkg.__file__}")
```

---

## New words

- **package**: a folder of Python modules with an `__init__.py` file.
- **dependency**: another package that your project needs.
- **virtual environment (venv)**: a private folder with its own Python and packages.
- **src layout**: a project layout where the real code is inside `src/`.
- **relative import**: an import that starts with `.` or `..`.
- **linter**: a tool that finds style problems and likely bugs.
- **editable install**: `pip install -e .`, which uses your source files directly.
