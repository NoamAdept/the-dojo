# Strength Classifier

`py-control-flow` · Blue Belt

**Goal:** Complete `classify_signal(snr)` and `summarize(values)` in `classify.py` so each SNR gets the label `weak`, `usable` or `strong`, and the counts come back as a dict.

**File `classify.py`**

```python
import sys

def classify_signal(snr):
    if snr < 5:
        return "weak"
    elif snr < 15:
        return "usable"
    else:
        return "strong"

def summarize(values):
    counts = {"weak": 0, "usable": 0, "strong": 0}
    for value in values:
        label = classify_signal(value)
        counts[label] = counts[label] + 1
    return counts

if __name__ == "__main__":
    values = [int(x) for x in sys.argv[1:]]
    print(summarize(values))
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
