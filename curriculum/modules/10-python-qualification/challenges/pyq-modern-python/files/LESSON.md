# Modern Python Features: lesson

### 1. Type Hints (Optional Static Typing)

Since Python 3.5, you can add type annotations (type hints) to variables and functions. Python ignores them when the code runs, so Python stays dynamic. But they are very important for static analysis (tools that check code without running it), such as mypy and IDE autocomplete.

```python
def calculate_total(price: float, tax_rate: float) -> float:
    return price * (1 + tax_rate)

result = calculate_total(100.0, 0.2)
print(f"Total: {result}")

# Annotating variables (Python 3.6+)
user_id: int = 42
username: str = "admin"

print(f"User: {username} ({user_id})")
```

### 2. Advanced Type Hints (`typing` module)

For collections and more complex types, we use the `typing` module. Since Python 3.9, you can also use the built-in generic types instead.

```python
from typing import List, Dict, Optional, Union

# List of integers
scores: List[int] = [10, 20, 30]

# Dictionary mapping string to integer
inventory: Dict[str, int] = {"apple": 5, "banana": 10}

# Optional: Can be int or None
def find_user(id: int) -> Optional[str]:
    if id == 1: return "Alice"
    return None

# Union: Can be int or float
number: Union[int, float] = 3.14
print(f"Found: {find_user(1)}")
print(f"Found: {find_user(99)}")
```

### 3. f-strings (Formatted String Literals)

F-strings came in Python 3.6. They give you a short, easy-to-read way to put expressions inside strings. They are also faster than %-formatting or `.format()`.

```python
name = "Python"
version = 3.10

# Basic interpolation
print(f"Language: {name}, Version: {version}")

# Expressions inside braces
print(f"Next version: {version + 0.1:.2f}")

# Debugging shortcut (Python 3.8+): variable_name=
x = 10
y = 25
print(f"{x=}, {y=}, {x+y=}")
```

### 4. Assignment Expressions (The Walrus Operator `:=`)

The `:=` operator came in Python 3.8. People call it the "walrus operator" because it looks like the eyes and teeth of a walrus. It lets you assign a value to a variable inside an expression. This helps you avoid repeating code, mostly in loops and `if` conditions.

```python
# Without walrus
data = [1, 2, 3, 4, 5]
n = len(data)
if n > 3:
    print(f"List is long ({n} elements)")

# With walrus
if (n := len(data)) > 3:
    print(f"List is long ({n} elements)")

# While loop example (simulated input)
inputs = ["data", "more data", "end", "ignored"]
it = iter(inputs)
while (val := next(it)) != "end":
    print(f"Processing: {val}")
```

### 5. Structural Pattern Matching (`match` / `case`)

Pattern matching came in Python 3.10. It is like a `switch` statement, but much more powerful. It lets you compare data structures with patterns. It can also take the parts out of the data (destructure it) in the same step.

```python
def process_command(command):
    match command:
        case "start":
            print("Starting...")
        case "stop":
            print("Stopping...")
        case ["move", direction]:
            print(f"Moving {direction}")
        case ["move", x, y]:
            print(f"Moving to ({x}, {y})")
        case _:
            print("Unknown command")

process_command(["move", "up"])
process_command(["move", 10, 20])
process_command("start")
```

### 6. Positional-Only and Keyword-Only Arguments

You can control how callers pass arguments:
- `/` makes the arguments before it positional-only (pass by position, not by name).
- `*` makes the arguments after it keyword-only (pass by name only).

```python
def standard_arg(arg):
    print(f"Standard: {arg}")

def pos_only_arg(arg, /):
    print(f"Pos only: {arg}")

def kw_only_arg(*, arg):
    print(f"KW only: {arg}")

standard_arg(1)
standard_arg(arg=1)

pos_only_arg(1)
# pos_only_arg(arg=1) # TypeError

kw_only_arg(arg=1)
# kw_only_arg(1) # TypeError
```

### 7. Data Classes (`@dataclass`)

Data classes came in Python 3.7. Many classes only store data. For these classes, `dataclasses` remove a lot of boilerplate (repeated code you would write by hand). They create `__init__`, `__repr__`, `__eq__` and other methods for you.

```python
from dataclasses import dataclass

@dataclass
class Point3D:
    x: float
    y: float
    z: float = 0.0

p1 = Point3D(1.5, 2.5)
p2 = Point3D(1.5, 2.5)

print(p1) # Auto-generated __repr__
print(f"Equal? {p1 == p2}") # Auto-generated __eq__
```

### 8. Dictionary Merging (`|` Operator)

Since Python 3.9, you can merge dictionaries with `|`.

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

d3 = d1 | d2
print(f"Merged: {d3}") # Note: d2 overwrote d1's 'b'
```

### 9. Ellipsis (`...`)

The `...` literal is called Ellipsis. It has 3 common uses:
- a placeholder for code you will write later (like `pass`),
- in type hints, to stand for "any number of" dimensions or items,
- in slicing.

```python
def to_be_implemented():
    ...

print(type(...))
```

### 10. Generic Aliases (3.9+)

You can now use built-in collection types like `list` and `dict` as generic types. You do not need to import `List` and `Dict` from `typing` anymore.

```python
# Python 3.9+
def scale(vector: list[float], factor: float) -> list[float]:
    return [x * factor for x in vector]

print(scale([1.0, 2.0], 2.0))
```

---

## New words

- **type hint**: a note about the expected type. Python does not enforce it.
- **walrus operator**: `:=`, which assigns a value inside an expression.
- **pattern matching**: `match`/`case`, which compares data with patterns and takes out its parts.
- **boilerplate**: repeated code that you must write but that does little.
- **dataclass**: a class that mainly stores data. Python writes the usual methods for you.
