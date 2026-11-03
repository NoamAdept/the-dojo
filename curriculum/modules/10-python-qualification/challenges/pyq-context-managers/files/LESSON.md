# Resource Management and Context Managers: lesson

### 1. The `with` Statement

A resource is something you must give back after use, such as a file, a lock or a connection. The `with` statement makes sure Python cleans up resources quickly and correctly. This happens even when an error occurs.

```python
# Without context manager (The hard way)
f = open("test_file.txt", "w")
try:
    f.write("Hello, World!")
finally:
    f.close()

# With context manager (The Pythonic way)
with open("test_file.txt", "w") as f:
    f.write("Hello again!")
# File is automatically closed here
```

### 2. How Context Managers Work (`__enter__` and `__exit__`)

A context manager is an object that you use with `with`. Any class can be a context manager. It needs 2 methods: `__enter__` (setup) and `__exit__` (teardown, which means cleanup). This matches the constructor and destructor logic of RAII in C++.

```python
class MyContext:
    def __enter__(self):
        print("Entering context...")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context...")
        # Return False to propagate exceptions, True to suppress them
        return False

with MyContext() as ctx:
    print("Inside block")
```

### 3. Handling Exceptions in `__exit__`

If an exception happened, the `__exit__` method gets information about it. So you can handle the error there. You can also make sure cleanup happens, on success and on failure.

```python
class ErrorSuppressor:
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"Suppressed ValueError: {exc_val}")
            return True # Suppress exception
        return False # Propagate others

with ErrorSuppressor():
    raise ValueError("Oops!")

print("Survived the error!")
```

### 4. `contextlib.contextmanager`

For simple resource management, you do not need a class. You can use a generator with the `@contextmanager` decorator instead.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Setup")
    try:
        yield "Resource"
    finally:
        print("Teardown")

with managed_resource() as r:
    print(f"Using {r}")
```

### 5. Nesting Context Managers

You can use more than 1 context manager in a single `with` statement.

```python
# Pseudo-code simulation
@contextmanager
def opener(name):
    print(f"Opening {name}")
    yield name
    print(f"Closing {name}")

with opener("A") as a, opener("B") as b:
    print(f"Processing {a} and {b}")
```

### 6. Common Use Cases: Locks

A lock lets only 1 thread use something at a time. Threading locks are context managers. So `with` always releases the lock for you. This prevents deadlocks (threads that wait for each other forever) caused by a forgotten release.

```python
import threading

lock = threading.Lock()

with lock:
    print("Critical section (Lock acquired automatically)")

# Lock released automatically
```

### 7. Common Use Cases: Timing

You can write a context manager that measures how long a block of code takes to run.

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.time()
    
    def __exit__(self, *args):
        print(f"Elapsed: {time.time() - self.start:.4f}s")

with Timer():
    sum(range(1000000))
```

### 8. Common Use Cases: Temporary Changes

Use context managers to change global state for a short time. For example, you can change the decimal precision or the working directory. The old value comes back at the end of the block.

```python
import decimal

print(f"Default precision: {decimal.getcontext().prec}")

with decimal.localcontext() as ctx:
    ctx.prec = 4
    print(f"Local precision: {decimal.Decimal(1) / decimal.Decimal(3)}")

print(f"Back to default: {decimal.getcontext().prec}")
```

---

## New words

- **resource**: something you must release after use, such as a file or a lock.
- **context manager**: an object with `__enter__` and `__exit__` that you use with `with`.
- **teardown**: the cleanup step at the end.
- **RAII**: a C++ idea. An object gets a resource when it is created and releases it when it is destroyed.
- **deadlock**: 2 or more threads wait for each other forever.
