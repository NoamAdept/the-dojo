# Strings and Dictionaries

**What you will learn:** how to clean up text and cut it into parts, and how to look up values by name with a dictionary.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`.

1. **clean_upper**: `clean_upper(text)` removes spaces and newlines from both ends. It returns the result in capitals. For example, `clean_upper("  fm radio\n")` returns `"FM RADIO"`.
2. **words**: `words(sentence)` returns the list of words in the sentence. Split on spaces.
3. **dashed**: `dashed(parts)` joins a list of strings, with `-` between them. For example, `dashed(["a", "b"])` returns `"a-b"`.
4. **make_station**: `make_station(name, freq)` returns a dict with the keys `"name"` and `"freq"`. The keys hold the two arguments.
5. **mode_of**: `mode_of(station)` returns `station["mode"]` if the dict has that key. If not, it returns `"FM"`.
6. **parse_pair**: `parse_pair(line)` splits a line like `"gain = 18"` at the **first** `=`. It returns a list of the two parts, with the spaces stripped: `["gain", "18"]`. For example, `"label = roof=antenna"` gives `["label", "roof=antenna"]`.
7. **count_words**: `count_words(sentence)` returns a dict of how many times each word appears. Upper case and lower case count as the same. For example, `count_words("Go go STOP")` returns `{"go": 2, "stop": 1}`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
