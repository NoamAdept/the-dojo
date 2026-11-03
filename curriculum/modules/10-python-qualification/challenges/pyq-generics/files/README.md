# Generics and Type Hinting



## Module 14: Generics & Type Hinting

Python is dynamically typed. This means Python finds out the types only when the code runs. But large modern Python projects depend a lot on **Static Type Checking**. Tools like mypy and pyright (mypy/pyright) check types without running the code. Generics let you write flexible code that you can reuse. The code is still type-safe.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Generic swap**: `swap(a: T, b: T) -> tuple[T, T]` with `T = TypeVar("T")`.
2. **Protocol**: `Clickable(Protocol)` with `click() -> str`, marked `@runtime_checkable`. `process_click(obj)` returns `obj.click()`. If `obj` is not Clickable, it raises `TypeError`.
3. **Literal status**: `Status = Literal["IDLE", "RUNNING", "ERROR"]`. `set_status(status)` returns the status. For any other value, it raises `ValueError`. Compare the value with `typing.get_args(Status)`.
4. **TypedDict**: `Car(TypedDict)` with `make: str`, `model: str` and `year: int`.
5. **Generic container**: `Stack(Generic[T])` with `push`, `pop`, `peek` and `__len__`. If the stack is empty, `pop` and `peek` raise `IndexError`.
6. **Typed observer**: `Observable(Generic[T])` with `subscribe(callback: Callable[[T], None])` and `notify(data: T)`.
7. **Plugin system**: `Plugin(Protocol)` with `name() -> str` and `execute(data: dict) -> dict`. `PluginManager` has `register` and `run_all(data)`. `run_all` passes the data through each plugin, in order. The output of one plugin is the input of the next. Also write 2 plugins:
   - `AuthPlugin` adds `"auth": True`.
   - `LogPlugin` appends its name to `data["log"]`, which is a list.

## Check your work

Run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
