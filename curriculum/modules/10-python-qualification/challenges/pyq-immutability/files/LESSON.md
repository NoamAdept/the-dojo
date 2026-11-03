# Immutability and State: lesson

### 1. Mutable vs Immutable Types

- **Immutable**: you cannot change the object's state (its data) after you create it. Some operations look like they change it. In fact, they create a new object.
    - Examples: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`.
- **Mutable**: you can change the object's state in place (without making a new object).
    - Examples: `list`, `dict`, `set`, `bytearray`, most classes that you write yourself.

```python
# Immutable String
s = "Hello"
print(f"Original ID: {id(s)}")
s = s + " World"
print(f"New ID: {id(s)} (Different object)")

# Mutable List
lst = [1, 2, 3]
print(f"List ID: {id(lst)}")
lst.append(4)
print(f"List ID: {id(lst)} (Same object)")
```

### 2. The `tuple`: An Immutable List

A `tuple` is roughly like a `const std::vector` or a fixed-size array in C++. After you create it, you cannot assign new values to its elements.

```python
t = (10, 20, 30)
print(t[0])

try:
    t[0] = 99
except TypeError as e:
    print(f"Error: {e}")
```

### 3. Tuple Unpacking

Python lets you unpack a tuple (or another iterable) straight into variables. Unpacking means you put each element into its own variable. People often use this to return more than 1 value from a function.

```python
coordinates = (15, 25)
x, y = coordinates
print(f"x={x}, y={y}")

# Swapping variables without temp
a = 1
b = 2
a, b = b, a
print(f"a={a}, b={b}")
```

### 4. `NamedTuple`: C-Struct Equivalent

You can use `collections.namedtuple` or `typing.NamedTuple`. The second one is the better choice. Both let you read fields by name, and the object stays immutable. They are very good for data-transfer objects (DTOs: simple objects that only carry data).

```python
from typing import NamedTuple

class Config(NamedTuple):
    host: str
    port: int

conf = Config("localhost", 8080)
print(f"Connecting to {conf.host}:{conf.port}")

# conf.port = 9000  # AttributeError: can't set attribute
```

### 5. `frozenset`: Immutable Set

A `tuple` is an immutable `list`. In the same way, a `frozenset` is an immutable `set`. It is immutable, so it is hashable. So you can use it as a dictionary key or as an element of another set.

```python
fs = frozenset([1, 2, 3])
print(fs)

try:
    fs.add(4)
except AttributeError as e:
    print(f"Error: {e}")

# Can be used as dict key
lookup = {fs: "My Immutable Set"}
print(lookup[fs])
```

### 6. Hashability and Dictionary Keys

An object must be **hashable** to be a key in a dictionary (map). Hashable means Python can compute a fixed number (a hash) for it, and that number never changes.
- Immutable built-in types are hashable.
- Mutable built-in types (`list`, `dict`) are NOT hashable.

```python
my_dict = {}

key_tuple = (1, 2)
key_list = [1, 2]

my_dict[key_tuple] = "Valid"
print("Tuple key worked.")

try:
    my_dict[key_list] = "Invalid"
except TypeError as e:
    print(f"List key failed: {e}")
```

### 7. Defining Constants (`Final`)

Python 3.8 added `typing.Final`. It does not stop you from assigning a new value while the program runs, as `const` would. But static analysis tools (tools that read code without running it) will report the new assignment.

```python
from typing import Final

PI: Final = 3.14159

# IDE/Linter would complain here, though runtime allows it
PI = 3.0 
print(f"PI is now {PI} (Python doesn't strictly enforce const)")
```

### 8. The "Default List" Trap

Mutable default arguments are a common Python trap. Python evaluates a default argument value **only once**, when it defines the function. It does not evaluate it again on each call. So every call shares the same list.

```python
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1)) # [1]
print(bad_append(2)) # [1, 2] !!! (The same list object is persisting)

def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1)) # [1]
print(good_append(2)) # [2] (Correct)
```

---

## New words

- **mutable**: can be changed after it is made.
- **immutable**: cannot be changed after it is made.
- **hashable**: has a fixed hash number, so it can be a dict key or a set element.
- **unpacking**: putting the elements of a tuple or list into separate variables.
- **memoize**: save the result of a function call, so the next call with the same arguments is fast.
