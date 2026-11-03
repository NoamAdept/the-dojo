# Collections and Comprehensions



## Module 7: Collections & Comprehensions

Python has strong built-in collections (containers for many values). Learn them well. Also learn the "comprehension" syntax. Both are key to writing Pythonic code (code in the normal Python style).

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **List filtering**: `multiples_of_three()` uses a comprehension. It returns the numbers from 0 to 20 that you can divide by 3.
2. **Dict inversion**: `invert(d)` swaps the keys and the values. Use a dict comprehension.
3. **Counter**: `word_counts(sentence)` returns a `Counter` of the words.
4. **DefaultDict**: `group_pairs(pairs)` puts `(key, value)` pairs into groups in a `defaultdict(list)`.
5. **Student grades**: `names_and_map(records)` returns `(names_list, name_to_grade_dict)`. Use comprehensions.
6. **Text analyzer**: `analyze_text(text)` does 3 things:
   - It changes the text to lowercase.
   - It removes punctuation.
   - It returns `{"total_words": n, "unique_words": n, "most_common_word": (word, count)}`.
7. **Moving average**: `MovingAverage(n)` uses `deque(maxlen=n)` and a running sum (a total you update on each step). `add(value)` returns the current average in O(1) time.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
