# Classes and Objects: lesson

### 1. Defining Classes

A class is a template for making objects. The syntax to define one is simple. In C++, each class often has its own file. Python does not require this. Still, people often put 1 large class in 1 file.

```python
class Robot:
    pass

r1 = Robot()
r2 = Robot()

print(r1)
print(f"Are they the same? {r1 is r2}")
```

### 2. The Constructor: `__init__`

Python uses a special method called `__init__` to set up (initialize) a new object. It does the same job as a constructor in C++.

```python
class Cyborg:
    def __init__(self, name, model):
        self.name = name   # Instance attribute
        self.model = model # Instance attribute
        print(f"Cyborg {name} initialized.")

c = Cyborg("T-800", 101)
```

### 3. The `self` Parameter

In C++, `this` is a hidden pointer that you can use inside methods. In Python, the method gets the object **explicitly** (you can see it). It is the first argument of every method. By convention (common agreement), we call it `self`.

```python
class Greeter:
    def say_hello(self):
        # Must use self to access other methods/attributes is needed, 
        # though here we just print.
        print(f"Hello from {self}")

g = Greeter()
g.say_hello() 
# Is equivalent to:
Greeter.say_hello(g)
```

### 4. Class Attributes vs Instance Attributes

- **Instance attributes**: variables that belong to 1 object. You create them in `__init__` with `self.var`.
- **Class attributes**: variables that all objects of the class share. You create them directly in the class body. They are the same as `static` members in C++.

```python
class NetworkNode:
    total_nodes = 0 # Class attribute

    def __init__(self, ip):
        self.ip = ip # Instance attribute
        NetworkNode.total_nodes += 1

n1 = NetworkNode("192.168.1.1")
n2 = NetworkNode("192.168.1.2")

print(f"Total nodes: {NetworkNode.total_nodes}")
```

### 5. Method Types

- **Instance method**: gets `self`. It can change the object's state (its data).
- **Class method** (`@classmethod`): gets `cls` (the class). It can change the class state. Factory methods (methods that build new objects) often look like this.
- **Static method** (`@staticmethod`): gets neither `self` nor `cls`. It is a normal function that lives inside the class namespace.

```python
class MathUtil:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def create(cls):
        return cls() # Returns an instance of the class

print(f"1 + 2 = {MathUtil.add(1, 2)}")
```

### 6. Encapsulation

Encapsulation means hiding an object's inner data. Python has no `private` or `protected` keywords. It uses naming conventions instead:
- `_variable`: protected. It is for internal use only. Please do not touch it from outside.
- `__variable`: private. Python changes the name (name mangling), so it is harder to reach from outside.

```python
class Account:
    def __init__(self):
        self.public = "I am public"
        self._protected = "I am internal"
        self.__private = "I am secret"

a = Account()
print(a.public)
print(a._protected) # Accessible, but linting will warn you
# print(a.__private) # AttributeError!
print(f"Secret accessed via mangling: {a._Account__private}")
```

### 7. Inheritance

A class can inherit (take over) the attributes and methods of a parent class. Python supports single and multiple inheritance. Use `super()` to call the parent classes.

```python
class Animal:
    def speak(self):
        print("...")

class Dog(Animal):
    def speak(self):
        super().speak() # Call parent
        print("Woof!")

d = Dog()
d.speak()
```

### 8. Magic Methods (`__str__` vs `__repr__`)

Magic methods (also called dunder methods, for "double underscore") have names that start and end with 2 underscores. Python calls them for you.
- `__str__`: for users. `print()` and `str()` call it.
- `__repr__`: for developers. The REPL (the interactive `>>>` prompt) calls it. Its output should be clear, with only 1 possible meaning.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p = Point(1, 2)
print(f"Str: {p}")
print(f"Repr: {repr(p)}")
```

### 9. Operator Overloading

Define `__add__`, `__sub__` and similar methods. Then operators such as `+` and `-` work on your objects.

```python
class Box:
    def __init__(self, items):
        self.count = items
    
    def __add__(self, other):
        return Box(self.count + other.count)

b1 = Box(10)
b2 = Box(5)
b3 = b1 + b2
print(f"Box 3 has {b3.count} items.")
```

### 10. Properties

The `@property` decorator lets you write methods that look like attributes from outside (getters and setters). This is the "Pythonic" (normal Python style) way to do encapsulation.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
c.radius = 10 
print(c.radius)
```

---

## New words

- **class**: a template that describes a kind of object.
- **instance**: 1 object made from a class.
- **attribute**: a variable that belongs to an object or a class.
- **dunder method**: a method with a name like `__add__`. Python calls it for you.
- **polymorphism**: different classes have the same method name, so callers can use them in the same way.
- **property**: a method that you use like an attribute.
