"""Python Qualification 07: collections and comprehensions."""
import re
from collections import Counter, defaultdict, deque


def multiples_of_three():
    return [n for n in range(21) if n % 3 == 0]


def invert(d):
    return {v: k for k, v in d.items()}


def word_counts(sentence):
    return Counter(sentence.split())


def group_pairs(pairs):
    groups = defaultdict(list)
    for key, value in pairs:
        groups[key].append(value)
    return groups


def names_and_map(records):
    return [name for name, _ in records], {name: grade for name, grade in records}


def analyze_text(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    counts = Counter(words)
    return {
        "total_words": len(words),
        "unique_words": len(counts),
        "most_common_word": counts.most_common(1)[0],
    }


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
