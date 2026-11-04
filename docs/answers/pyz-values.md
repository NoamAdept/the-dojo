# Variables, Types and f-strings

`pyz-values` · Blue Belt

**Goal:** Replace every `None` in `tasks.py` with a value of the right type, a conversion, or an f-string.

**File `tasks.py`**

```python
"""Python from Zero 02: variables, types and f-strings."""

station = "Pi Radio"
channels = 16
gain_db = 20.5
is_on = True

text_number = "433"
as_int = int(text_number)

label = f"{station} has {channels} channels"

pi = 3.14159
pi_text = f"{pi:.2f}"
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
