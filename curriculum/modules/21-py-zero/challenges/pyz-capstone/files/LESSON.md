# Capstone: a Command-line Program: lesson

### 1. Raising an error yourself

Sometimes a function gets input that it cannot handle. Then do not return a wrong answer. Stop the function
with an error that says why:

```python
def parse_age(text):
    if not text.isdigit():
        raise ValueError(f"not a number: {text!r}")
    return int(text)
```

`raise` stops the function at once. It is like `return`, but for errors. `ValueError` is Python's standard
error for "this value has the wrong shape". `{text!r}` shows the value with quotes around it. So you can
see empty text or text with only spaces in the message.

### 2. Command-line arguments: sys.argv

`import sys` is already at the top of `report.py`. It loads `sys`, a built-in **module** of Python. A module
is only a `.py` file of ready-made code. For example, `tasks.py` was a module that `./check` imported.
`sys.argv` is the list of words on the command line. It is exactly like `argv` in C++'s
`int main(int argc, char* argv[])`:

```console
$ python3 report.py readings.txt
```

This command gives `sys.argv == ["report.py", "readings.txt"]`. So the file name is `sys.argv[1]`.

### 3. The main check

`./check` imports `report.py` to test your functions one at a time. When it does this, the whole program
must not run. Python sets the special variable `__name__` to `"__main__"` only in one case: when you run the
file directly with `python3 report.py`. So put the "run the program" part under this test, at the bottom of
the file:

```python
if __name__ == "__main__":
    main(sys.argv[1])
```

Now `python3 report.py readings.txt` runs `main`. But `import report` only defines the functions.

### The data

`readings.txt` holds one reading on each line, in the form `station,snr`. SNR is the signal-to-noise ratio.
It is a whole number. A bigger number means a clearer signal. Lines that start with `#` are comments. The
same station can appear more than once:

```text
# station,snr
tower,12
beacon,4
tower,15
```

`read_lines` and `write_lines` from the last challenge are already in `report.py`. They are finished. One
more built-in function helps: `sorted(d)` on a dict gives a list of its keys in order. For strings, the
order is alphabetical.

**New words**
- raise: stop with an error on purpose.
- ValueError: the standard error for "this value has the wrong shape".
- module: a `.py` file of code that you can `import`, like `sys` or your own `tasks.py`.
- sys.argv: the list of command-line words. `sys.argv[1]` is the first argument after the script name.
- `__name__ == "__main__"`: True only when you run the file directly. False when another file imports it.

## Offline help

- Offline: `python3 -m pydoc sys` and `python3 -m pydoc raise`
