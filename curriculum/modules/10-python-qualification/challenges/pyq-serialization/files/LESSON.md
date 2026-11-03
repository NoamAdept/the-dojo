# Dataclasses and Serialization: lesson

### 1. Review: Dataclasses

A dataclass is a class that mainly holds data. `@dataclass` writes these methods for you automatically: `__init__`, `__repr__`, `__eq__`. You can also add your own methods and default values.

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str = ""
    active: bool = True

u = User(1, "alice", "alice@example.com")
print(u)
```

### 2. Converting Dataclasses to/from Dicts

The `dataclasses` module gives you 2 helper functions: `asdict` and `astuple`. They connect dataclasses to JSON, because JSON works with dicts and lists (dicts/lists).

```python
from dataclasses import asdict, astuple

user_dict = asdict(u)
print(f"Dict: {user_dict}")

user_tuple = astuple(u)
print(f"Tuple: {user_tuple}")

# Recreating from dict (**kwargs)
u2 = User(**user_dict)
print(f"Recreated: {u2}")
```

### 3. JSON Serialization

Serialization means turning an object into text or bytes, so you can save it or send it. JSON is a standard text format for sharing data. The `json` module supports only basic types:

- `dict`, `list`
- `str`, `int`, `float`, `bool`
- `None`

```python
import json

data = {
    "users": [
        {"name": "Alice", "id": 1},
        {"name": "Bob", "id": 2}
    ],
    "meta": {"count": 2}
}

json_str = json.dumps(data, indent=2)
print(json_str)

parsed = json.loads(json_str)
print(f"Parsed Count: {parsed['meta']['count']}")
```

### 4. Custom JSON Encoders

By default, JSON does not support complex objects, like your own classes or `datetime`. You must tell it how to handle them. One way is to pass a function with `default=`. The function turns the object into basic types.

```python
class ComplexObj:
    def __init__(self, val):
        self.val = val

def obj_encoder(o):
    if isinstance(o, ComplexObj):
        return {"__complex__": True, "val": o.val}
    raise TypeError(f"Object of type {type(o)} is not JSON serializable")

c = ComplexObj(42)
print(json.dumps(c, default=obj_encoder))
```

### 5. Pickle (Binary Serialization)

`pickle` is a binary format. Only Python can read it, and it is efficient. It can serialize almost ANY Python object (even functions!).

**WARNING**: Never unpickle (load) data from a source you do not trust. Unpickling can run any code (arbitrary code) that the attacker put in the data.

```python
import pickle

complex_data = {"set": {1, 2, 3}, "obj": c} # Set and Obj aren't JSON-safe defaults

serialized = pickle.dumps(complex_data)
print(f"Pickle bytes (hex): {serialized[:20].hex()}...")

restored = pickle.loads(serialized)
print(f"Restored Set: {restored['set']}")
```

### 6. Binary File I/O

Binary data is data that is not plain text: pickles, images, data packed with `struct`. To save or load it, usually open the file with mode `wb` (write binary) and `rb` (read binary).

```python
with open("data.pkl", "wb") as f:
    pickle.dump([1, 2, 3], f)

with open("data.pkl", "rb") as f:
    content = pickle.load(f)
    print(f"Loaded: {content}")
```

### 7. Introduction to `pydantic`

`dataclasses` from the standard library do not validate (check) types at runtime. `pydantic` does check them. Many modern web APIs use it (for example FastAPI).

*(Note: pydantic may not be installed on your Pi. So the example below is a small, simple copy of what pydantic does.)*

```python
# Simplified simulation of what Pydantic does
class PydanticLite:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            expected_type = self.__annotations__.get(k)
            if expected_type and not isinstance(v, expected_type):
                # Try to cast
                try:
                    v = expected_type(v)
                except:
                    raise TypeError(f"Expected {k} to be {expected_type}")
            setattr(self, k, v)

class Config(PydanticLite):
    port: int

c = Config(port="8080") # String converted to int!
print(f"Validated Port: {c.port} (Type: {type(c.port)}) ")
```

### 8. Making Classes Immutable with Dataclasses

`frozen=True` makes a dataclass immutable. This means you cannot change its fields after you create it. It is like a `NamedTuple`, but you get all the features of a class.

```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(10, 20)
try:
    p.x = 30 # AttributeError
except Exception as e:
    print(f"Immutable: {e}")
```

---

## New words

- **dataclass**: a class that mainly holds data. `@dataclass` writes the common methods for you.
- **serialization**: turning an object into text or bytes, to save or send it.
- **deserialization**: turning text or bytes back into an object.
- **JSON**: a standard text format for data. Many languages can read it.
- **pickle**: Python's own binary format. Only load pickles that you trust.
- **immutable**: cannot be changed after it is created.
- **validate**: check that a value has the right type or form.
