## Classify Signal Strengths

*py-control-flow · easy*

**Goal.** Complete `classify_signal(snr)` and `summarize(values)` in `classify.py` so each SNR gets the label `weak`, `usable` or `strong`, and the counts come back as a dict.

**You need to know.**

- `if` / `elif` / `else` runs only the first true branch (README lesson 2, and pyz-if).
- Boundaries: 4 is weak, 5 is usable, 14 is usable, 15 is strong (README lesson 3).
- Counting into a dict that starts every label at 0 (README lesson 4).
- Functions must `return`, because `./check` imports the file and calls them (README lesson 1).

**Walkthrough.**

1. Run the starter to see the problem.

   ```bash
   python3 classify.py 2 8 19
   ```

   It prints `None`, because both functions only contain `pass` and so return nothing.

2. Write `classify_signal`, replacing the `pass`.

   ```python
   def classify_signal(snr):
       if snr < 5:
           return "weak"
       elif snr < 15:
           return "usable"
       else:
           return "strong"
   ```

   The `elif` is only reached when `snr >= 5`, so it only needs the upper edge; `< 15` keeps 14 usable and makes 15 strong. Negative numbers fall into `weak`.

3. Write `summarize`, replacing its `pass`.

   ```python
   def summarize(values):
       counts = {"weak": 0, "usable": 0, "strong": 0}
       for value in values:
           label = classify_signal(value)
           counts[label] = counts[label] + 1
       return counts
   ```

   All three keys exist from the start, so a label that never appears still shows 0; each value is classified with the function from step 2 and its counter goes up by one.

4. Leave the `if __name__ == "__main__":` block as it is, and try the program again.

   ```bash
   python3 classify.py 2 8 19
   ```

   It now prints `{'weak': 1, 'usable': 1, 'strong': 1}`.

5. Run the check.

   ```bash
   ./check
   ```

**Check.** `./check` prints `CHECK_OK` (it is silent about passing cases and prints `Not yet: ...` for the first failure). Press Done in the dojo to get the flag.

**Common mistakes.**

- `snr <= 5` or `snr < 14`: off by one at a boundary. The check tests -3, 4, 5, 14, 15 and 99 and names the failing value.
- Starting with `counts = {}`: then `counts[label] + 1` raises `KeyError`, and missing labels are not in the result.
- Using `print` inside the functions instead of `return`.
