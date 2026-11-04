# Typed Packet Router

`pyq-modern-python` · Blue Belt

**Goal:** Use modern syntax in `tasks.py`: `f"{x=}"` debugging, the walrus operator, dataclasses, the dict `|` merge, and structural pattern matching with `match` / `case`.

**File `tasks.py`**

```python
"""Python Qualification 06: modern Python features."""
from dataclasses import dataclass

def debug_line(a, b):
    return f"{a=}, {b=}, {a*b=}"

def drain(words):
    out = []
    while words and (w := words.pop()):
        out.append(w)
    return out

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True

def merge(defaults, user):
    return defaults | user

def describe_shape(shape):
    match shape:
        case ("circle", r):
            return f"circle r={r}"
        case ("rect", w, h):
            return f"rect {w}x{h}"
        case _:
            return "unknown"

def load_config(path: str) -> dict[str, int | str]:
    match path.rsplit(".", 1)[-1]:
        case "json":
            return {"format": "json", "version": 1}
        case "txt":
            return {"format": "text", "lines": 0}
        case ext:
            raise ValueError(f"unsupported config type: {ext}")

@dataclass
class ConnectPacket:
    ip: str
    port: int

@dataclass
class DataPacket:
    id: int
    payload: bytes

@dataclass
class DisconnectPacket:
    id: int

def parse_packet(p):
    match p:
        case ("CONNECT", str(ip), int(port)):
            return ConnectPacket(ip, port)
        case ("DATA", pid, payload):
            return DataPacket(pid, payload)
        case ("DISCONNECT", pid):
            return DisconnectPacket(pid)
        case _:
            raise ValueError(f"bad packet: {p!r}")
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
