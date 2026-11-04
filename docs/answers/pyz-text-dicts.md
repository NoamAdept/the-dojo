# Strings and Dictionaries

`pyz-text-dicts` · Blue Belt

**Goal:** Write seven functions in `tasks.py` that clean, split and join strings, and build, read and count with dictionaries.

**File `tasks.py`**

```python
"""Python from Zero 07: strings and dictionaries."""

def clean_upper(text):
    return text.strip().upper()

def words(sentence):
    return sentence.split()

def dashed(parts):
    return "-".join(parts)

def make_station(name, freq):
    return {"name": name, "freq": freq}

def mode_of(station):
    return station.get("mode", "FM")

def parse_pair(line):
    key, value = line.split("=", 1)
    return [key.strip(), value.strip()]

def count_words(sentence):
    counts = {}
    for word in sentence.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
