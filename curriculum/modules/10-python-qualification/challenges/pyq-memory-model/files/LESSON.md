# References and the Memory Model: lesson

### 1. Variables are Labels, Not Boxes

In C++, `int x = 10;` reserves (allocates) memory for an integer and gives it the name `x`.
In Python, `x = 10` creates an integer object `10` somewhere in memory. Then it attaches the label `x` to that object.

People often call this **Call by Object Reference**. A reference is a pointer to an object.

```python
x = [1, 2, 3]
y = x

# Both x and y refer to the SAME object
print(f"ID x: {id(x)}")
print(f"ID y: {id(y)}")

y.append(4)
print(f"x is also modified: {x}")
```

### 2. The `id()` Function

`id(obj)` returns the "identity" of an object. In CPython (the normal Python program), this is in practice the object's memory address. You should not depend on that, though. Python promises that the id is unique and does not change while the object exists.

```python
a = "Hello"
b = "Hello"

# String interning may cause these to be standard
print(f"a is b? {a is b}") 
print(f"id(a) == id(b)? {id(a) == id(b)}")
```

### 3. Reference Counting

Python mainly uses **reference counting** to manage memory. Each object counts how many references point to it. When the count drops to 0, Python frees (deallocates) the object at once.

```python
import sys

obj = [1, 2, 3]
# ref count is 2: 1 for 'obj', 1 for getrefcount argument itself
print(f"Ref count: {sys.getrefcount(obj)}") 

other = obj
print(f"Ref count after alias: {sys.getrefcount(obj)}")
```

### 4. `is` vs `==`

- `is`: checks identity (is it the same object?). It is a fast pointer comparison.
- `==`: checks equality (is it the same value?). It calls `__eq__`, and it can be slow.

```python
x = [1, 2, 3]
y = [1, 2, 3]

print(f"x == y: {x == y} (Values are equal)")
print(f"x is y: {x is y} (Different objects)")
```

### 5. Garbage Collection (GC)

Reference counting does not work with **circular references** (objects that point at each other in a circle). Their counts never reach 0. So Python also has a cyclic garbage collector. It runs from time to time. It finds these circles and frees them.

```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None
    
    def __del__(self):
        print(f"{self.name} deleted")

def create_cycle():
    n1 = Node("A")
    n2 = Node("B")
    n1.link = n2
    n2.link = n1
    # n1 and n2 go out of scope here using ref count, but cycle remains
    print("Cycle created and abandoned")

create_cycle()
print("Forcing GC...")
gc.collect()
```

### 6. Weak References

A **weak reference** (made with `weakref`) lets you point to an object without adding 1 to its reference count. This is useful for caches. The GC can still free the objects when nothing else uses them.

```python
import weakref

class HeavyObject:
    pass

obj = HeavyObject()
weak = weakref.ref(obj)

print(f"Weak ref resolves to: {weak()}")
del obj
print(f"Weak ref after delete: {weak()}")
```

### 7. Argument Passing Model

Python passes arguments by assignment. In practice, this means:
- A function can change a mutable object that you pass to it.
- If the function assigns a new value to the argument name (`param = ...`), only the local label changes. The caller's variable stays the same.

```python
def modify(lst, num):
    lst.append("Added") # Mutates object
    num = 100           # Rebinds local name

my_list = []
my_num = 1
modify(my_list, my_num)

print(f"List: {my_list}")
print(f"Num: {my_num}")
```

### 8. Shallow Copy

`copy.copy` creates a new container. But it puts references to the original items into it. It does not copy the items.

```python
import copy

orig = [[1], [2]]
shallow = copy.copy(orig)

shallow[0].append(9)
print(f"Original: {orig} (See how it changed?)")
```

### 9. Deep Copy

`copy.deepcopy` copies the object and everything inside it, level by level (recursively). This costs more time and memory, but it is safe.

```python
orig = [[1], [2]]
deep = copy.deepcopy(orig)

deep[0].append(9)
print(f"Original: {orig} (Unmodified)")
print(f"Deep: {deep}")
```

### 10. Interning (Optimization)

Python caches (keeps and reuses) small integers, usually -5 to 256, and some strings. This is called interning. It is an implementation detail of CPython. Do not depend on it in your program logic.

```python
a = 256
b = 256
print(f"256 is 256: {a is b}")

a = 257
b = 257
print(f"257 is 257: {a is b} (Likely False, depends on environment)")
```

---

## New words

- **reference**: a pointer to an object. A variable name is a reference.
- **identity**: which object it is. You check it with `is` or `id()`.
- **reference count**: how many references point to an object.
- **garbage collector (GC)**: the part of Python that frees objects nobody can reach.
- **shallow copy**: a new outer container that shares the inner objects.
- **deep copy**: a full copy, including all inner objects.
