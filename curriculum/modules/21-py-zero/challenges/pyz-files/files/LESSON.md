# Reading and Writing Files: lesson

### Reading a file

`open(path)` opens a file for reading. `with` makes sure that Python closes the file again when the indented
block ends. It does this even if something goes wrong. It is like a C++ `std::ifstream`, which closes the file
by itself when it goes out of scope (when the code block that made it ends):

```python
with open("notes.txt") as f:
    for line in f:
        print(line.strip())
```

`f` is a name for the open file. Any name works, but `f` is common. When you loop over a file, you get one
line at a time. Each line is a string that **still ends with `"\n"`**. That is why we `strip()` it. Here is
another way to read:

```python
with open("notes.txt") as f:
    text = f.read()          # the whole file as one string
```

The path is relative to the folder you run Python from. This is the same as in the shell. If the file is
missing, you get a `FileNotFoundError`. The error message names the file.

### Skipping lines

Real data files often have blank lines. They also often have comment lines that start with `#`. After
`strip()`, a blank line is the empty string `""`. In an `if`, an empty string counts as False. Any other
string counts as True. So you can write:

```python
line = line.strip()
if line and not line.startswith("#"):
    keep.append(line)        # only real data lines get here
```

### Writing a file

To write, give `"w"` (write) as the second argument to `open`. This creates the file. If the file already
exists, it **empties** it first. So be careful which name you use. `write` does not add a newline for you:

```python
with open("out.txt", "w") as f:
    f.write("first line\n")
    f.write(f"value: {42}\n")
```

Then look at the result in the shell: `cat out.txt`.

**New words**
- file: named data on disk. A text file is lines of characters. Each line ends in `\n`.
- open: start to use a file. `open(path)` reads. `open(path, "w")` writes (and empties the file first).
- with: a block that closes the file by itself when the block ends.
- `"\n"`: the newline character at the end of each line.
- FileNotFoundError: the error you get when the file you open does not exist.

## Offline help

- Offline: `python3 -m pydoc open` and `python3 -m pydoc with`
