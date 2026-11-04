# Reading and Writing Files

`pyz-files` · Blue Belt

**Goal:** Write five functions in `tasks.py` that read a file whole, count its lines, read clean lines, write lines, and combine read and write into `shout_file`.

**File `tasks.py`**

```python
"""Python from Zero 08: reading and writing files."""

def read_all(path):
    with open(path) as f:
        return f.read()

def count_lines(path):
    count = 0
    with open(path) as f:
        for line in f:
            count += 1
    return count

def read_lines(path):
    lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

def write_lines(path, lines):
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")

def shout_file(src, dst):
    write_lines(dst, [line.upper() for line in read_lines(src)])
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
