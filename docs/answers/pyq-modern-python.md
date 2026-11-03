## Modern Python Features

*pyq-modern-python · medium*

**Goal.** Use modern syntax in `tasks.py`: `f"{x=}"` debugging, the walrus operator, dataclasses, the dict `|` merge, and structural pattern matching with `match` / `case`.

**You need to know.**

- `f"{expr=}"` prints the expression text and its value (Python 3.8+).
- `:=` assigns inside an expression.
- `@dataclass` and default field values.
- `a | b` merges dicts into a new dict (Python 3.9+).
- `match` with sequence patterns, class patterns like `int(port)`, and `case _:`.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1. Each `{x=}` expands to `x=<value>`, including the expression `a*b`.

   ```python
   def debug_line(a, b):
       return f"{a=}, {b=}, {a*b=}"
   ```

3. Task 2. The walrus pops and tests in one step. The check also greps for `:=`, so it must be used.

   ```python
   def drain(words):
       out = []
       while words and (w := words.pop()):
           out.append(w)
       return out
   ```

4. Task 3. Replace the comment with the dataclass; `in_stock` gets a default so it must come last.

   ```python
   @dataclass
   class Product:
       name: str
       price: float
       in_stock: bool = True
   ```

5. Task 4. `|` builds a new dict, and the right side wins on duplicate keys. The original `defaults` is not changed.

   ```python
   def merge(defaults, user):
       return defaults | user
   ```

6. Task 5. A sequence pattern matches on both length and the literal first item.

   ```python
   def describe_shape(shape):
       match shape:
           case ("circle", r):
               return f"circle r={r}"
           case ("rect", w, h):
               return f"rect {w}x{h}"
           case _:
               return "unknown"
   ```

7. Task 6. Match on the text after the last dot. A bare name like `ext` in the last case catches everything else.

   ```python
   def load_config(path: str) -> dict[str, int | str]:
       match path.rsplit(".", 1)[-1]:
           case "json":
               return {"format": "json", "version": 1}
           case "txt":
               return {"format": "text", "lines": 0}
           case ext:
               raise ValueError(f"unsupported config type: {ext}")
   ```

8. Task 7. Define three dataclasses, then match. `int(port)` matches only when the third item is an int, so `("CONNECT", "x", "80")` falls through to `case _` and raises.

   ```python
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

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Writing `case ("CONNECT", ip, port):` without `int(...)`, so the string port is accepted and no `ValueError` is raised.
- Using `defaults.update(user)` in `merge`, which changes the caller's dict; the check makes sure it is untouched.
- Leaving out `case _:` in `parse_packet`; then a bad packet like `("PING",)` falls off the end and returns `None` instead of raising.
