# Functions: def and return: lesson

A **function** is a piece of code with a name. You can run it again and again. In C++ you wrote:

```cpp
int add(int a, int b) {
    return a + b;
}
```

In Python the same function is:

```python
def add(a, b):
    return a + b

print(add(2, 3))     # prints: 5
```

Here are the parts, one by one:
- `def` starts a function **definition**. `add` is its name.
- `a` and `b` are its **parameters**. They are names for the values the function gets. You do not write types.
- The line ends with a **colon** `:`.
- The **body** is every line below that is **indented** (moved to the right, usually by 4 spaces). Python uses
  indentation instead of `{ }` in C++. So indentation is not only style. The indent tells Python which lines
  belong to the function. The first line that is not indented ends the body.
- `return` gives a value back to the code that **called** the function. It also leaves the function at once.

**Calling** a function means running it, for example `add(2, 3)`. The values in the brackets are the **arguments**.

**return is not print.** `print` only shows a value on the screen. The caller gets nothing. `return` gives the
value back. Then the caller can store it or use it:

```python
def shown(x):
    print(x * 2)       # shows it, gives back nothing

def given(x):
    return x * 2       # gives it back

a = shown(5)   # screen shows 10, but a is None
b = given(5)   # screen shows nothing, b is 10
```

A function with no `return` gives back `None`. `./check` tests your functions. It calls them and looks at
what they **return**. So always use `return` here.

Functions can call other functions that you wrote:

```python
def add_three(a, b, c):
    return add(add(a, b), c)
```

**The starter stubs.** A stub is an empty function that you must fill in. Each function in `tasks.py` now has one line in its body:

```python
def double(n):
    """Task 1: return n times 2."""
    raise NotImplementedError
```

The text in triple quotes is a **docstring**. It describes the function. `raise NotImplementedError`
makes the function stop with a "not done yet" error. `./check` reports this as "not implemented yet".
Delete that `raise` line. Write your own body in its place, with the same indentation.

Before you run the check, try a function at the prompt:

```console
$ python3
>>> import tasks
>>> tasks.double(4)
8
```

(If you edit `tasks.py`, leave the prompt with `exit()`. Then start it again to load the new version.)

**New words**
- function: a block of code with a name. You can use it many times.
- def: the keyword that defines a function.
- parameter: a name in the `def` line. It stands for a value the function receives.
- argument: the real value you pass when you call a function, like the `4` in `double(4)`.
- return: give a value back to the caller and leave the function.
- indentation: the spaces at the start of a line. In Python they decide which lines belong to a block.
- docstring: the text in triple quotes at the top of a function. It describes the function.
- stub: an empty function that you must fill in.

## Offline help

- Offline: `python3 -m pydoc def` and `python3 -m pydoc return`
