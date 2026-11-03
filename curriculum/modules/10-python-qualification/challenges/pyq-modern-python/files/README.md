# Modern Python Features



## Module 6: Modern Python Features

Python changes quickly. "Modern Python" (Python 3.6 and newer) adds features that make code clearer, safer and cleaner. This module covers the most important modern features.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **F-string debugging**: `debug_line(a, b)` returns `f"{a=}, {b=}, {a*b=}"`. The result looks like `"a=10, b=20, a*b=200"`.
2. **Walrus loop**: `drain(words)` uses `while (w := ...)` to pop items from the end of the list until the list is empty. It returns them in the order it popped them.
3. **Dataclass**: write `Product(name: str, price: float, in_stock: bool = True)`.
4. **Dictionary merge**: `merge(defaults, user)` returns a new dict built with `|`. When a key is in both, the user setting wins.
5. **Shape matcher**: `describe_shape(shape)` uses `match` on tuples.
   - `("circle", r)` gives `"circle r=5"`.
   - `("rect", w, h)` gives `"rect 10x20"`.
   - Anything else gives `"unknown"`.
6. **Typed config loader**: `load_config(path: str) -> dict[str, int | str]` uses `match` on the file extension.
   - `.json` returns `{"format": "json", "version": 1}`.
   - `.txt` returns `{"format": "text", "lines": 0}`.
   - Any other extension raises `ValueError`.
7. **Packet parser**: `parse_packet(p)` matches 3 packet shapes:
   - `("CONNECT", ip, port)` returns a `ConnectPacket` dataclass.
   - `("DATA", id, payload)` returns a `DataPacket` dataclass.
   - `("DISCONNECT", id)` returns a `DisconnectPacket` dataclass.

   A packet with any other shape raises `ValueError`. `port` must be an int.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
