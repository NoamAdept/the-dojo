# Generics and Type Hinting: lesson

### 1. Review: Basic Types

A type hint tells readers and tools what type a value should have. You already know these basic hints:

- `list[int]`
- `dict[str, int]`
- `Optional[int]`
- `Union[int, str]` (or `int | str`)

```python
def process_items(items: list[str]) -> int:
    return len(items)

# process_items([1, 2, 3]) # Debugger/Linter would flag this
```

### 2. TypeVar (The "T" in Templates)

A generic function works with many types, but keeps the types connected. For example, "the output has the same type as the input". In C++ you use `template <typename T>` for this. In Python, you use `TypeVar`.

```python
from typing import TypeVar, List

T = TypeVar("T")

def first(container: List[T]) -> T:
    return container[0]

x = first([1, 2, 3])       # T is inferred as int
y = first(["a", "b"])      # T is inferred as str
# z: int = first(["a"])    # Type Checker Error
```

### 3. Generic Classes

A class can also be generic. To do this, inherit from `Generic[T]`.

```python
from typing import Generic

class Box(Generic[T]):
    def __init__(self, item: T):
        self.item = item
    
    def get(self) -> T:
        return self.item

int_box = Box(10)
str_box = Box("Hello")
```

### 4. Bounded TypeVars

You can limit `T` with a bound. Then `T` must be a specific type or a subclass of it. This is like C++ Concepts or Java `extends`.

```python
class Animal: 
    pass

class Dog(Animal):
    pass

A = TypeVar("A", bound=Animal)

def pet(animal: A) -> A:
    return animal

pet(Dog()) # OK
# pet(10)  # Error: int is not bound by Animal
```

### 5. Protocols (Structural Subtyping / Duck Typing)

This is the most useful feature of Python static typing. Duck typing means: if an object has the right methods, you can use it. A Protocol describes **what** an object needs to do. The object does not need to inherit from anything. This is called structural subtyping.

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

def render(obj: Drawable):
    obj.draw()

class Circle: # Does NOT inherit from Drawable!
    def draw(self):
        print("Circle")

render(Circle()) # Passes type check because it conforms to the structure
```

### 6. Callable Types

Use `Callable` to give a type hint for a function that you pass as an argument.

```python
from typing import Callable

# Function taking two ints and returning an int
Operation = Callable[[int, int], int]

def execute(op: Operation, x: int, y: int):
    print(op(x, y))

execute(lambda a, b: a + b, 5, 10)
```

### 7. Literal Types

A `Literal` type allows only a fixed set of exact values. It is like an enum, but you do not need to write a class.

```python
from typing import Literal

Mode = Literal["r", "w", "rb", "wb"]

def open_file(mode: Mode):
    print(f"Opening in {mode}")

open_file("r")
# open_file("x") # Type error
```

### 8. Runtime Type Checking

Remember: everything above is for **Static Analysis**. Static analysis means that a tool reads your code without running it. By default, Python checks NOTHING about types at runtime (when the code runs). If you need checks at runtime, use `isinstance`. You can also use libraries like `typeguard`.

```python
def runtime_checked(x: int):
    if not isinstance(x, int):
        raise TypeError(f"Expected int, got {type(x)}")
    print(x)

runtime_checked(10)
# runtime_checked("10") # Raises TypeError
```

---

## New words

- **type hint**: a note in the code that says what type a value should have.
- **static type checker**: a tool (like mypy or pyright) that finds type errors without running the code.
- **generic**: code that works with many types and keeps them connected.
- **TypeVar**: a placeholder for a type, often called `T`.
- **bound**: a limit on a TypeVar. `T` must be that type or a subclass.
- **Protocol**: a description of the methods an object must have.
- **duck typing**: you use an object because of its methods, not its class.
- **runtime**: the time when the program actually runs.
