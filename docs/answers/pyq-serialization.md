# Dataclasses and Serialization

`pyq-serialization` · Blue Belt

**Goal:** Define dataclasses (one frozen), save and load data with `json` and `pickle`, and build a `file_cache` decorator that keeps results in a pickle file between runs.

**File `tasks.py`**

```python
"""Python Qualification 12: dataclasses and serialization."""
import functools
import json
import os
import pickle
from dataclasses import asdict, dataclass

@dataclass
class Item:
    name: str
    price: float

def student_json():
    return json.dumps({"name": "John", "grades": [80, 90]})

def pickle_roundtrip(obj):
    data = pickle.dumps(obj)
    print(data)
    return data, pickle.loads(data)

@dataclass(frozen=True)
class Settings:
    debug: bool

def save_config(config, filename):
    with open(filename, "w") as fh:
        json.dump(config, fh, indent=2)

def load_config(filename):
    with open(filename) as fh:
        return json.load(fh)

@dataclass
class User:
    name: str
    age: int

def serialize_users(users, filename):
    with open(filename, "w") as fh:
        json.dump([asdict(u) for u in users], fh)

def deserialize_users(filename):
    with open(filename) as fh:
        return [User(**row) for row in json.load(fh)]

def file_cache(filename):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(x):
            cache = {}
            if os.path.exists(filename):
                with open(filename, "rb") as fh:
                    cache = pickle.load(fh)
            if x not in cache:
                cache[x] = func(x)
                with open(filename, "wb") as fh:
                    pickle.dump(cache, fh)
            return cache[x]
        return wrapper
    return decorator
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
