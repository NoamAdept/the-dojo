# Variables, Types and f-strings: lesson

**Variables.** A **variable** is a name that points to a value. You make one with `=`:

```python
channels = 16
print(channels)        # prints: 16
channels = channels + 1
print(channels)        # prints: 17
```

In C++ you wrote `int channels = 16;`. The type `int` could never change. In Python there is no type in front of the name.
The **type** (the kind of value) belongs to the value, not to the name. Python finds the type itself.

Rules for names:

- They can use letters, digits and `_`.
- They cannot start with a digit.
- They are case sensitive. `Gain` and `gain` are different names.

**The basic types.** To see the type of a value, ask Python with `type(...)`:

```console
>>> type(16)
<class 'int'>
>>> type(20.5)
<class 'float'>
>>> type("Pi Radio")
<class 'str'>
>>> type(True)
<class 'bool'>
```

- `int`: a whole number, like `16` or `-3`. Python ints never overflow (become too big to store). `2 ** 100` works fine.
- `float`: a number with a decimal point, like `20.5`. It is like `double` in C++.
- `str`: a string (text) in quotes.
- `bool`: a truth value, either `True` or `False`. Note the capital letters.

There is one more special value, **`None`**. It means "nothing here yet". The starter file uses it for
every value that you still need to fill in.

**Converting.** You cannot mix text and numbers. `"433" + 1` gives a `TypeError`. Convert the value first:

```python
int("433")      # 433, the text turned into an int
float("2.5")    # 2.5
str(7)          # "7", the number turned into text
```

**f-strings.** You can put values inside text. Write `f` just before the opening quote. Then put any variable or
sum inside `{ }`:

```python
freq = 433
print(f"Listening on {freq} MHz")       # Listening on 433 MHz
print(f"Double is {freq * 2}")          # Double is 866
print(f"{3.14159:.2f}")                 # 3.14
```

Inside the braces, after a `:`, you can say how to format the number. `.2f` means "2 digits after the point".
It is like `std::fixed << std::setprecision(2)` in C++. An f-string is a normal `str`. So you can also store it in a variable.

**How this challenge is checked.** You edit `tasks.py`. `./check` **imports** it. This means it loads the file and reads its
variables. Then it tests the values. You can try your file yourself at any time:

- Run `python3 tasks.py`. It prints nothing unless you add prints.
- Or look at it at the prompt:

```console
$ python3
>>> import tasks
>>> tasks.station
```

**New words**
- variable: a name that points to a value. You make it with `name = value`.
- type: the kind of a value (int, float, str, bool). See it with `type(x)`.
- None: a special value meaning "nothing yet".
- conversion: making a value of one type from another, like `int("433")`.
- f-string: a string with `f` in front. Python replaces each `{expression}` inside it with its value.
- import: loading a `.py` file, so another program can use what is inside it.
- overflow: when a number becomes too big for its type. Python ints do not overflow.

## Offline help

- Offline: `python3 -m pydoc int`, `python3 -m pydoc str`, `python3 -m pydoc FORMATTING`
