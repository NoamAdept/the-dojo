# Data Types and Dynamic Typing: lesson

### 1. Dynamic vs Static Typing

In C++, you give each variable a type when you declare it (`int x;`). After that, the variable can only hold integers. Think of it as a box with the label "Integer".

In Python, a variable is only a **name tag**. You can put the tag `x` on an integer. Later you can take the tag off and put it on a string. The *value* has a type. The *variable* does not.

```python
x = 10
print(f"x is {x}, type: {type(x)}")

x = "Now I'm a string"
print(f"x is '{x}', type: {type(x)}")

# This flexibility comes at a runtime cost, but offers rapid development speed.
```

### 2. Integers: Arbitrary Precision

C++ integers have a fixed size (32-bit or 64-bit). They can overflow (go past the largest value and wrap around). Python integers are objects. They grow automatically to fit the number. You can calculate $2^{1000}$ without any extra library.

```python
tiny_int = 5
huge_int = 2 ** 100

print(f"Tiny: {tiny_int}")
print(f"Huge: {huge_int}")
print(f"Type of huge_int: {type(huge_int)}") # Still just 'int'
```

### 3. Floating Point Numbers

A Python `float` is the same as a C++ `double` (64-bit IEEE 754). Standard Python has no single-precision `float` like C++ has. Libraries such as NumPy do have one.

```python
val = 0.1 + 0.2
print(f"0.1 + 0.2 = {val}")
print(f"Equal to 0.3? {val == 0.3} (Standard floating point quirk)")
```

### 4. Strings: The `str` Type

Python strings use Unicode by default. They are also **immutable** (they cannot change). You cannot change one character inside a string. You must make a new string instead.

```python
s = "Hello, World!"

# Slicing (very powerful)
print(s[0:5])   # "Hello"
print(s[::-1])  # Reverse string: "!dlroW ,olleH"

# Immutability check
try:
    s[0] = 'h'
except TypeError as e:
    print(f"Error: {e}")
```

### 5. F-Strings (Formatted String Literals)

F-strings came in Python 3.6. They are the usual way to format strings today. They are faster and easier to read than `%` or `.format()`.

```python
name = "Alice"
score = 95.234

print(f"Player: {name}, Score: {score:.2f}")
print(f"Math: 2 + 2 = {2 + 2}")
```

### 6. Booleans and Truthiness

Python has `True` and `False`. Many other values also count as "False" when Python needs a yes/no answer. We call these values "falsy":
- `0`, `0.0`
- Empty sequences: `""`, `[]`, `()`
- `None`

```python
items = []

if not items:
    print("List is empty (Falsy)")

value = 0
if value:
    print("Value is True")
else:
    print("Value is False")
```

### 7. Strong Typing

Python is dynamic, but it is also **strongly typed**. It will not guess how to join two types that do not match. For example, it will not add a string to an integer.

```python
a = 10
b = "20"

try:
    print(a + b)
except TypeError as e:
    print(f"Cannot add int and str: {e}")

# Must explicitly cast
print(f"Sum: {a + int(b)}")
```

### 8. `None` Type

`None` is a special object that means "no value". There is only one `None` object in a program (it is a singleton). It does a similar job to `nullptr` or `NULL` in C++. The difference is that `None` is a real object.

```python
val = None

if val is None:
    print("Value is None")

# None is often used as a default value for optional arguments
```

### 9. Type Checking

Use `isinstance()` to check a type while the program runs. Do not use `type(x) == T`. It gives the wrong answer for subclasses (it breaks inheritance).

```python
num = 50
if isinstance(num, int):
    print(f"{num} is an integer")

if isinstance(num, (int, float)):
    print(f"{num} is a number")
```

### 10. Type Hints (Optional Static Typing)

Modern Python lets you add types to variables and functions. We call these type hints. Python itself ignores them when the code runs. Tools such as mypy and IDEs (code editors) use them to find mistakes before the code runs. This is called static analysis.

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

# Valid Python, even if we violate the hint (runtime ignores it)
print(greet("Alice"))
print(greet(123))
```

---

## New words

- **dynamic typing**: the type belongs to the value, not to the variable name.
- **strong typing**: Python will not mix types that do not match without you asking.
- **immutable**: cannot be changed after it is made.
- **slice**: a part of a sequence, written `s[start:stop]`.
- **falsy**: a value that counts as `False` in an `if` test.
- **type hint**: a note about the expected type. Python does not enforce it.

## Offline help

- Offline: `python3 -m pydoc int`
