## Collections and Comprehensions

*pyq-collections · easy*

**Goal.** Implement six functions and the `MovingAverage` class in `tasks.py` using comprehensions and the `collections` module (`Counter`, `defaultdict`, `deque`).

**You need to know.**

- List and dict comprehensions.
- `Counter`, `defaultdict(list)` and `deque(maxlen=n)` from `collections`.
- `re.findall` for pulling words out of text.
- `Counter.most_common(1)`.

**Walkthrough.**

1. Run `./check` to see the seven failing tasks.

   ```bash
   ./check
   ```

2. Task 1, list filtering. `range(21)` includes 20; the `if` keeps multiples of 3.

   ```python
   def multiples_of_three():
       return [n for n in range(21) if n % 3 == 0]
   ```

3. Task 2, dict inversion. Swap the order of the pair in the comprehension.

   ```python
   def invert(d):
       return {v: k for k, v in d.items()}
   ```

4. Task 3, Counter. `split()` gives the words and `Counter` tallies them. Return the Counter itself, not a plain dict.

   ```python
   def word_counts(sentence):
       return Counter(sentence.split())
   ```

5. Task 4, defaultdict. A missing key starts as an empty list, so `append` always works.

   ```python
   def group_pairs(pairs):
       groups = defaultdict(list)
       for key, value in pairs:
           groups[key].append(value)
       return groups
   ```

6. Task 5, student grades. Two comprehensions over the same records, returned as a tuple.

   ```python
   def names_and_map(records):
       return [name for name, _ in records], {name: grade for name, grade in records}
   ```

7. Task 6, text analyzer. Add `import re` at the top. Lowercasing first means "The" and "the" count as one word, and the regex drops `!`, `,` and `.`.

   ```python
   def analyze_text(text):
       words = re.findall(r"[a-z0-9']+", text.lower())
       counts = Counter(words)
       return {
           "total_words": len(words),
           "unique_words": len(counts),
           "most_common_word": counts.most_common(1)[0],
       }
   ```

8. Task 7, moving average. Keep a running total. When the deque is full, the oldest value (`window[0]`) is about to fall out, so subtract it before appending. Each `add` is O(1).

   ```python
   class MovingAverage:
       def __init__(self, n):
           self.window = deque(maxlen=n)
           self.total = 0

       def add(self, value):
           if len(self.window) == self.window.maxlen:
               self.total -= self.window[0]
           self.window.append(value)
           self.total += value
           return self.total / len(self.window)
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Subtracting `window[0]` after `append`: by then the old value has already been dropped, so the wrong number is removed from the total.
- In `analyze_text`, splitting on spaces leaves `"pi!"` and `"antenna."` as words, so the counts are wrong.
- In `MovingAverage`, storing the values in a plain list or forgetting `maxlen`; the check looks for a `deque` with `maxlen == 3` in the instance attributes.
