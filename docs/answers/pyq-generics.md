## Generics and Type Hinting

*pyq-generics · medium*

**Goal.** Use the `typing` module in `tasks.py`: a `TypeVar`, a runtime-checkable `Protocol`, a `Literal`, a `TypedDict`, two `Generic[T]` classes and a small plugin system built on a protocol.

**You need to know.**

- `TypeVar("T")` and `Generic[T]` (so `Stack[int]()` is legal).
- `Protocol` checks shape, not inheritance; `@runtime_checkable` allows `isinstance`.
- `Literal[...]` and `typing.get_args`.
- `TypedDict` and `Callable[[T], None]`.

**Walkthrough.**

1. Run `./check` to see the failures. All the needed names are already imported at the top.

   ```bash
   ./check
   ```

2. Task 1. Annotate with `T`; the check reads the hints and expects `tuple[T, T]` as the return type.

   ```python
   def swap(a: T, b: T) -> tuple[T, T]:
       return b, a
   ```

3. Task 2. Any object with a `click` method now counts as `Clickable`.

   ```python
   @runtime_checkable
   class Clickable(Protocol):
       def click(self) -> str: ...

   def process_click(obj: Clickable) -> str:
       if not isinstance(obj, Clickable):
           raise TypeError(f"{obj!r} is not Clickable")
       return obj.click()
   ```

4. Task 3. Type hints are not enforced at runtime, so check the value yourself against `get_args(Status)`.

   ```python
   Status = Literal["IDLE", "RUNNING", "ERROR"]

   def set_status(status: Status) -> Status:
       if status not in get_args(Status):
           raise ValueError(f"invalid status {status!r}")
       return status
   ```

5. Task 4. A `TypedDict` is a plain dict at runtime with known keys for type checkers.

   ```python
   class Car(TypedDict):
       make: str
       model: str
       year: int
   ```

6. Task 5. Subclass `Generic[T]`; raise `IndexError` yourself in `peek` (a list's `[-1]` would raise it too, but with a less clear message).

   ```python
   class Stack(Generic[T]):
       def __init__(self) -> None:
           self._items: list[T] = []
       def push(self, item: T) -> None:
           self._items.append(item)
       def pop(self) -> T:
           if not self._items:
               raise IndexError("pop from empty stack")
           return self._items.pop()
       def peek(self) -> T:
           if not self._items:
               raise IndexError("peek at empty stack")
           return self._items[-1]
       def __len__(self) -> int:
           return len(self._items)
   ```

7. Task 6. Keep a list of callbacks and call each one with the data, in order.

   ```python
   class Observable(Generic[T]):
       def __init__(self) -> None:
           self._subscribers: list[Callable[[T], None]] = []
       def subscribe(self, callback: Callable[[T], None]) -> None:
           self._subscribers.append(callback)
       def notify(self, data: T) -> None:
           for callback in self._subscribers:
               callback(data)
   ```

8. Task 7. The manager feeds each plugin's output into the next. The plugins do not inherit from `Plugin`; they only match its shape.

   ```python
   class Plugin(Protocol):
       def name(self) -> str: ...
       def execute(self, data: dict) -> dict: ...

   class PluginManager:
       def __init__(self) -> None:
           self._plugins: list[Plugin] = []
       def register(self, plugin: Plugin) -> None:
           self._plugins.append(plugin)
       def run_all(self, data: dict) -> dict:
           for plugin in self._plugins:
               data = plugin.execute(data)
           return data

   class AuthPlugin:
       def name(self) -> str:
           return "auth"
       def execute(self, data: dict) -> dict:
           return {**data, "auth": True}

   class LogPlugin:
       def name(self) -> str:
           return "log"
       def execute(self, data: dict) -> dict:
           return {**data, "log": [*data.get("log", []), self.name()]}
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Forgetting `@runtime_checkable`; then `isinstance(obj, Clickable)` raises `TypeError` for every object, including good ones.
- Writing `class Stack:` without `Generic[T]`, so `Stack[int]()` fails with "type 'Stack' is not subscriptable".
- In `run_all`, calling `plugin.execute(data)` without assigning the result back to `data`, so the plugins do not chain.
