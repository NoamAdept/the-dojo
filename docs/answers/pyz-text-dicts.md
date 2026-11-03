## Strings and Dictionaries

*pyz-text-dicts · easy*

**Goal.** Write seven functions in `tasks.py` that clean, split and join strings, and build, read and count with dictionaries.

**You need to know.**

- String methods `strip()`, `upper()`, `lower()`, `split()`, `startswith()` return new strings (README lesson).
- `"-".join(list_of_strings)` glues strings together.
- Dict literals `{"key": value}`, `d[key]`, and `d.get(key, default)`.
- The counting pattern `counts[w] = counts.get(w, 0) + 1`.

**Walkthrough.**

1. Open `tasks.py` and replace each `raise NotImplementedError`.

2. Tasks 1 to 3: string methods, one line each.

   ```python
   def clean_upper(text):
       return text.strip().upper()

   def words(sentence):
       return sentence.split()

   def dashed(parts):
       return "-".join(parts)
   ```

   `strip()` removes spaces, tabs and newlines at both ends and `upper()` works on the result. `split()` with no argument splits on any run of whitespace and ignores spaces at the ends. `join` is called on the separator and puts it between the items.

3. Task 4: build a dict.

   ```python
   def make_station(name, freq):
       return {"name": name, "freq": freq}
   ```

   The keys are strings in quotes; the values are the arguments.

4. Task 5: read a key that may be missing.

   ```python
   def mode_of(station):
       return station.get("mode", "FM")
   ```

   `get` returns the value when the key exists and the default `"FM"` when it does not, with no `KeyError`.

5. Task 6: split at the first `=` only.

   ```python
   def parse_pair(line):
       key, value = line.split("=", 1)
       return [key.strip(), value.strip()]
   ```

   The `1` means "split at most once", so `"label = roof=antenna"` keeps `roof=antenna` together. Each part is stripped of its spaces.

6. Task 7: count words.

   ```python
   def count_words(sentence):
       counts = {}
       for word in sentence.lower().split():
           counts[word] = counts.get(word, 0) + 1
       return counts
   ```

   Lower-casing first makes `Go` and `go` the same key; `get(word, 0)` starts a new word at 0. An empty sentence gives `{}`.

7. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- `sentence.split(" ")` in task 2: with extra spaces it returns empty strings, and the check tests `"  spaced   out  "`.
- `line.split("=")` without the `1` in task 6: the second `=` makes three parts.
- `station["mode"]` in task 5 crashes with `KeyError` when the key is missing.
