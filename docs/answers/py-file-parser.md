# Config Crypt

`py-file-parser` · Blue Belt

**Goal:** Complete `parse_config(path)` in `parse_config.py` so it turns `name = value` lines into a dict of strings, skips blanks and `#` comments, and raises `ValueError` on a line with no `=`. Running the script writes `parsed.txt`.

**File `parse_config.py`**

```python
import sys

def parse_config(path):
    """Return a dict from name=value lines; ignore blanks and # comments."""
    result = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("line without '=': " + line)
            name, value = line.split("=", 1)
            result[name.strip()] = value.strip()
    return result

if __name__ == "__main__":
    config = parse_config(sys.argv[1])
    with open("parsed.txt", "w") as out:
        for key in sorted(config):
            out.write(f"{key}={config[key]}\n")
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
