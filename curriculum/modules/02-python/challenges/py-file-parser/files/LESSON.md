# Parse a Config File: lesson

### 1. What a config file is

A configuration ("config") file is a plain text file of settings. A
program reads it when the program starts. Open receiver.conf to see one:

```
# classroom receiver        <- a comment, for humans only
frequency = 145800000
mode= FM                    <- spacing is not always neat
                            <- an empty line
label = roof=antenna        <- the VALUE itself contains "="
```

### 2. Reading a file line by line

```
with open(path) as f:
    for line in f:
        line = line.strip()     # removes spaces and the newline
```

`strip()` removes spaces, tabs and the invisible newline at both ends of
the line. After `strip()`, an empty line becomes "" (an empty string).

### 3. Skipping lines

`continue` jumps directly to the next turn of the loop. Use it to skip
empty lines and comment lines:

```
if line == "" or line.startswith("#"):
    continue
```

### 4. Splitting only once

- "a=b=c".split("=") gives ['a', 'b', 'c']. That is three pieces. This
  is wrong for us.
- "a=b=c".split("=", 1) splits at the FIRST "=" only: ['a', 'b=c'].

Then strip each piece, so " FM" becomes "FM".

You can put two names on the left of one "=". Python then puts the two
pieces into the two names at once. This is called unpacking:

```
name, value = "mode= FM".split("=", 1)
```

### 5. Raising an error on purpose

Look at a line that:

- is not blank,
- is not a comment,
- has no "=".

Then the file is broken. Do not guess what it means. Stop the function
with an exception (a signal that something went wrong):

```
if "=" not in line:
    raise ValueError("line without '=': " + line)
```

`raise` ends the function at once. It reports the problem to the caller
(the code that called the function). ValueError is Python's built-in name
for "this value is not acceptable". `./check` gives your function a broken
file. It expects exactly this error.

### 6. Docstrings

Look at the text in triple quotes just under `def parse_config(path):`.
This is a docstring. It is a short description of what the function must
do. Read it.

Values stay strings. Return "18", not the number 18. `./check` compares
your dictionary with a dictionary where all values are strings.

## New words
- **config file**: a text file of settings. It usually has name = value lines.
- **comment**: a line for humans. The program ignores it. Here it starts with #.
- **strip()**: removes whitespace (spaces, tabs, newlines) from both ends of a string.
- **continue**: skip the rest of this loop turn. Go to the next one.
- **exception**: a signal that something went wrong. It stops the normal flow of the program.
- **raise**: start an exception on purpose.
- **ValueError**: the built-in exception for "bad value".
- **docstring**: the description string written just under a def line.
- **unpack**: put the pieces of a list into several names at once.
