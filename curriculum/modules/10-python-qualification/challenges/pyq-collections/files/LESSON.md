# Collections and Comprehensions: lesson

### 1. The List (`list`)

A list is a dynamic array (an array that can grow and shrink). It is like `std::vector` in C++. It can hold values of different types. Usually, all its elements have the same type.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits.insert(1, "apricot")

print(f"Fruits: {fruits}")

# Removal
popped = fruits.pop() # Removes last
print(f"Popped: {popped}")
```

### 2. The Dictionary (`dict`)

A dict is a hash map (a table that finds a value from a key very fast). It is like `std::unordered_map` in C++. Keys must be hashable (Python can compute a fixed hash number for them). Since Python 3.7, a dict keeps the order in which you added the keys.

```python
ages = {"Alice": 30, "Bob": 25}
ages["Charlie"] = 35

print(f"Bob's age: {ages['Bob']}")

# Safe access
print(f"David's age: {ages.get('David', 'Unknown')}")

# Iteration
for name, age in ages.items():
    print(f"{name}: {age}")
```

### 3. The Set (`set`)

A set is a collection of unique elements with no fixed order. It is like `std::unordered_set` in C++. Use it to test quickly if a value is inside. You can also do math operations on sets, such as union and intersection.

```python
primes = {2, 3, 5, 7}
evens = {2, 4, 6, 8}

print(f"Union: {primes | evens}")
print(f"Intersection: {primes & evens}")
print(f"Difference: {primes - evens}")
```

### 4. List Comprehensions

A list comprehension is a short way to build a list. It often replaces `map()` and `filter()`.
Syntax: `[expression for item in iterable if condition]`

```python
numbers = [1, 2, 3, 4, 5]

# Square every number
squares = [x**2 for x in numbers]
print(f"Squares: {squares}")

# Filter even numbers
evens = [x for x in numbers if x % 2 == 0]
print(f"Evens: {evens}")
```

### 5. Dict and Set Comprehensions

Dicts and sets have a similar syntax.

```python
names = ["Alice", "Bob", "Charlie"]

# Dict comprehension: Name -> Length
name_lengths = {name: len(name) for name in names}
print(f"Lengths: {name_lengths}")

# Set comprehension: Unique squares
nums = [1, 2, 2, 3, 3, 3]
unique_squares = {x**2 for x in nums}
print(f"Unique Squares: {unique_squares}")
```

### 6. Generator Expressions

Use round brackets `()` instead of square brackets `[]`. This makes a generator. A generator gives you items one at a time, only when you ask (lazy evaluation). It saves memory.

```python
import sys

large_list = [x for x in range(1000)]
large_gen = (x for x in range(1000))

print(f"List size: {sys.getsizeof(large_list)} bytes")
print(f"Gen size: {sys.getsizeof(large_gen)} bytes")

# Consume generator
print(f"Sum: {sum(large_gen)}")
```

### 7. `collections.defaultdict`

A defaultdict creates a default value for you when a key is missing. You no longer need `dict.setdefault`.

```python
from collections import defaultdict

# Default value for int is 0
counts = defaultdict(int)
words = ["apple", "banana", "apple", "cherry"]

for w in words:
    counts[w] += 1

print(dict(counts))
```

### 8. `collections.Counter`

A Counter is a special dict for counting hashable objects. It is good for histograms (counts of how often each value appears).

```python
from collections import Counter

c = Counter("mississippi")
print(f"Most common: {c.most_common(2)}")
```

### 9. `collections.deque`

A deque is a double-ended queue (a queue you can use from both ends). Adding and removing at both ends is fast: O(1), so the time does not grow with the size. A list is O(n) when you remove from the front, so it gets slower as the list grows.

```python
from collections import deque

d = deque([1, 2, 3])
d.appendleft(0)
d.append(4)
print(d)
d.popleft()
```

### 10. Itertools

The `itertools` module gives you fast iterators (objects that give items one by one). Examples are permutations, combinations, and loops that never end.

```python
import itertools

colors = ["red", "green"]
sizes = ["S", "M"]

# Cartesian product
for item in itertools.product(colors, sizes):
    print(item)
```

---

## New words

- **comprehension**: a short syntax that builds a list, dict or set in 1 line.
- **hashable**: a value with a fixed hash, so it can be a dict key or a set element.
- **generator**: an object that makes items one at a time, only when needed.
- **O(1)**: the time stays the same, even when the collection gets bigger.
- **O(n)**: the time grows with the size of the collection.

## Offline help

- Offline: `python3 -m pydoc collections`
