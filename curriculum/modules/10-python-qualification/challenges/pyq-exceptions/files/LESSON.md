# Error and Exception Handling: lesson

### 1. Basic Try-Except

An exception is an error object that Python raises (throws) when something goes wrong. Put code that might raise an exception inside `try`. Use `except` to catch the exception.

```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("Caught division by zero!")

# Catching multiple types
try:
    val = int("not a number")
except (ValueError, TypeError):
    print("Invalid conversion.")
```

### 2. Capturing the Exception Object

Add `as e` to get the exception object itself. It usually holds a helpful message.

```python
try:
    f = open("non_existent_file.txt")
except FileNotFoundError as e:
    print(f"File error: {e}")
    print(f"Error Type: {type(e).__name__}")
```

### 3. The `else` Block

The `else` block runs **only when no exception happens**. Use it for code that must run only on success. Code in `else` is not protected by the `except` block, and that is what you want here.

```python
try:
    num = int("10")
except ValueError:
    print("Conversion failed.")
else:
    print(f"Conversion successful: {num}")
    # logic here is safe from being caught by 'except ValueError'
```

### 4. The `finally` Block

The `finally` block always runs. It runs when an exception happens, and it runs when no exception happens. The usual use is cleanup, such as closing a file. (For cleanup, `with` is usually the better choice.)

```python
try:
    print("Working...")
    # raise RuntimeError("Boom")
finally:
    print("Cleanup (Always runs)")
```

### 5. Raising Exceptions

Use `raise` to start an exception yourself. You can raise built-in exception types or your own types.

```python
def sqrt(x):
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return x ** 0.5

try:
    sqrt(-1)
except ValueError as e:
    print(e)
```

### 6. Custom Exceptions

You can make your own exception types. Inherit from `Exception` (not from `BaseException`).

```python
class NetworkError(Exception):
    pass

class ConnectionTimeout(NetworkError):
    def __init__(self, host):
        super().__init__(f"Timed out connecting to {host}")
        self.host = host

try:
    raise ConnectionTimeout("192.168.1.5")
except NetworkError as e:
    print(f"Network Issue: {e}")
```

### 7. Exception Chaining (`raise from`)

Sometimes you catch one exception and raise a different one. Then use `raise NewException from OldException`. This keeps the traceback (the record of where the error came from). This is very important for debugging.

```python
def internal_logic():
    raise KeyError("Key not found")

def public_api():
    try:
        internal_logic()
    except KeyError as e:
        # Transform implementation detail into public error
        raise RuntimeError("Data corruption") from e

try:
    public_api()
except RuntimeError as e:
    print(f"Caught: {e}")
    print(f"Caused by: {e.__cause__}")
```

### 8. EAFP vs LBYL

- **LBYL**: Look Before You Leap. First check the conditions, then act.
- **EAFP**: Easier to Ask Forgiveness than Permission. Just try to act, and catch the error if it fails.

Python often prefers EAFP. One reason is race conditions: the situation can change between your check and your action. Another reason is atomicity: trying in 1 step is safer than checking and acting in 2 steps.

```python
test_dict = {}

# LBYL
if "key" in test_dict:
    val = test_dict["key"]
else:
    val = None

# EAFP
try:
    val = test_dict["key"]
except KeyError:
    val = None
```

---

## New words

- **exception**: an error object that stops the normal flow of the code.
- **raise**: start (throw) an exception.
- **catch**: handle an exception in an `except` block.
- **traceback**: the report that shows where an exception came from.
- **race condition**: a bug where the result depends on the timing of 2 things.
