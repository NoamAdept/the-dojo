## References and the Memory Model

*pyq-memory-model · medium*

**Goal.** Write small functions in `tasks.py` that demonstrate identity vs equality, shallow copies, reference counts, the cycle garbage collector, object ids, a hand-made deep copy and a weak reference.

**You need to know.**

- `is` (same object) vs `==` (same value), and `id()`.
- `copy.copy` copies only the outer container.
- `sys.getrefcount` counts references to an object.
- Reference cycles are only freed by `gc.collect()`.
- `weakref.ref(obj)` returns a callable that gives the object or `None`.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1. Two list literals make two separate objects with equal content.

   ```python
   def identity_report():
       a, b = [1, 2, 3], [1, 2, 3]
       return a is b, a == b
   ```

3. Task 2. The shallow copy shares the inner list, so appending through the copy also changes the original.

   ```python
   def shallow_trap():
       original = {"a": [1, 2]}
       dup = copy.copy(original)
       dup["a"].append(3)
       return original
   ```

4. Task 3. Each new name or list slot pointing at the object adds one to its refcount.

   ```python
   def refcount_growth():
       obj = object()
       readings = [sys.getrefcount(obj)]
       alias = obj
       readings.append(sys.getrefcount(obj))
       holder = [obj]
       readings.append(sys.getrefcount(obj))
       return readings
   ```

5. Task 4. Two objects that point at each other keep each other's refcount above zero after `del`, so only the cycle collector frees them and `gc.collect()` returns a positive count.

   ```python
   class _Node:
       def __init__(self):
           self.peer = None

   def collect_cycle():
       a, b = _Node(), _Node()
       a.peer, b.peer = b, a
       del a, b
       return gc.collect()
   ```

6. Task 5. `n += 1` on an int makes a new int object and rebinds `n`, so its id changes.

   ```python
   def track_id(obj):
       return obj, id(obj)

   def int_id_changes():
       n = 1000
       before = id(n)
       n += 1
       return id(n) != before
   ```

7. Task 6. Recurse into dicts and lists; return anything else (tuples, strings, numbers) as is. The check confirms the tuple is shared, not copied.

   ```python
   def my_deepcopy(data):
       if isinstance(data, dict):
           return {k: my_deepcopy(v) for k, v in data.items()}
       if isinstance(data, list):
           return [my_deepcopy(v) for v in data]
       return data
   ```

8. Task 7. The blob references itself, so `del blob` does not free it. The weak ref still sees it (True). After `gc.collect()` it is gone (False). The check disables automatic GC while it runs this so the result is stable.

   ```python
   def cycle_needs_gc():
       blob = Blob()
       blob.other = blob
       ref = weakref.ref(blob)
       del blob
       before = ref() is not None
       gc.collect()
       after = ref() is not None
       return before, after
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- Using `copy.deepcopy` in task 2, so the original does not change and the "trap" is not shown.
- In task 7, checking `ref()` before `del blob`, or keeping another name to the blob, so it is never collected.
- In `my_deepcopy`, also converting tuples to lists, which breaks equality with the source.
