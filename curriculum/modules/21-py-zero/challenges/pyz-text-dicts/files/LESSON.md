# Strings and Dictionaries: lesson

### Strings

A string works a lot like a list of characters:

- `len("radio")` is 5.
- `"radio"[0]` is `"r"`.
- `"radio"[1:3]` is `"ad"`.

But you can never change a string in place. So string **methods** (functions that you call with a dot)
always give back a **new** string:

```python
"  fm radio \n".strip()       # "fm radio"   removes spaces and newlines at both ends
"Fm Radio".upper()            # "FM RADIO"
"Fm Radio".lower()            # "fm radio"
"a-b".replace("-", "+")       # "a+b"
"gain=18".startswith("gain")  # True
```

(`\n` is the newline character, as in C++.) When you call `text.upper()`, it does not change `text`. You must
store the result: `text = text.upper()`. You can chain methods (call one after the other):
`text.strip().lower()`.

**split** cuts a string into a list of strings. With no argument, it splits on any group of spaces. With an
argument, it splits on exactly that text. `split("=", 1)` splits only once, at most:

```python
"the quick  fox".split()        # ["the", "quick", "fox"]
"12,7,30".split(",")            # ["12", "7", "30"]
"label = a=b".split("=", 1)     # ["label ", " a=b"]
```

**join** does the opposite. It joins a list of strings together. It puts the string that you call it on
between each pair:

```python
"-".join(["a", "b", "c"])       # "a-b-c"
" ".join(["fm", "radio"])       # "fm radio"
```

### Dictionaries

A **dictionary** (`dict`) stores values under **keys**. It is like a C++ `std::map`, or like a phone book.
You look things up by name, not by position.

```python
station = {"name": "Pi Radio", "freq": 433.92}
station["name"]             # "Pi Radio"
station["gain"] = 18        # add a new key, or change an existing one
"freq" in station           # True: is this key present?
station.get("mode", "AM")   # "AM": the value, or a default if the key is missing
len(station)                # 3
```

If you ask for a missing key with square brackets, like `station["mode"]`, Python raises a `KeyError`.
`.get` does not have this problem. Loop over a dict to get its keys. Or use `.items()` to get each key and
its value together:

```python
for key, value in station.items():
    print(key, value)
```

**Counting with a dict** is a pattern that you will use all the time. Start with an empty dict. Then, for
each thing, do one of two things:

- If the thing is not in the dict yet, add it with count 1.
- If it is already there, add 1 to its count.

```python
counts = {}
for colour in ["red", "blue", "red"]:
    if colour in counts:
        counts[colour] += 1
    else:
        counts[colour] = 1
# counts is {"red": 2, "blue": 1}
```

(A shorter way to write the `if` is `counts[colour] = counts.get(colour, 0) + 1`.)

**New words**
- strip / upper / lower / replace: string methods that return a cleaned or changed copy.
- split: cut a string into a list of pieces.
- join: join a list of strings into one string, with a separator between them.
- dictionary (dict): a collection of key and value pairs, written `{key: value}`.
- key: the name that you use to look up a value in a dict.
- KeyError: the error you get when you ask a dict for a key that it does not have.

## Offline help

- Offline: `python3 -m pydoc str.split`, `python3 -m pydoc str.join`, `python3 -m pydoc dict`
