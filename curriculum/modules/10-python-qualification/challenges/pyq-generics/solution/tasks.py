"""Python Qualification 14: generics and type hinting."""
from typing import Callable, Generic, Literal, Protocol, TypedDict, TypeVar, get_args, runtime_checkable

T = TypeVar("T")


def swap(a: T, b: T) -> tuple[T, T]:
    return b, a


@runtime_checkable
class Clickable(Protocol):
    def click(self) -> str: ...


def process_click(obj: Clickable) -> str:
    if not isinstance(obj, Clickable):
        raise TypeError(f"{obj!r} is not Clickable")
    return obj.click()


Status = Literal["IDLE", "RUNNING", "ERROR"]


def set_status(status: Status) -> Status:
    if status not in get_args(Status):
        raise ValueError(f"invalid status {status!r}")
    return status


class Car(TypedDict):
    make: str
    model: str
    year: int


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


class Observable(Generic[T]):
    def __init__(self) -> None:
        self._subscribers: list[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]) -> None:
        self._subscribers.append(callback)

    def notify(self, data: T) -> None:
        for callback in self._subscribers:
            callback(data)


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
