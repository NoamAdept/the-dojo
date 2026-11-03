## Classes and Objects

*pyq-oop · medium*

**Goal.** Write the classes in `tasks.py`: a simple class, a class counter, operator overloading, a validated property, a bank account, polymorphic shapes and a small library system with private storage.

**You need to know.**

- `__init__`, instance attributes and class attributes.
- Dunder methods `__sub__`, `__eq__`, `__str__`, `__len__`.
- `@property` with a `.setter`.
- Inheritance and overriding a method.
- Name mangling for `self.__name` attributes.

**Walkthrough.**

1. Run `./check` to see the failures.

   ```bash
   ./check
   ```

2. Task 1, `Vehicle`. Store both arguments and return the string.

   ```python
   class Vehicle:
       def __init__(self, make, model):
           self.make, self.model = make, model
       def drive(self):
           return "Vroom"
   ```

3. Task 2, `Item`. The counter lives on the class, so update it through the class name.

   ```python
   class Item:
       count = 0
       def __init__(self):
           Item.count += 1
   ```

4. Task 3, `Vector`. `__sub__` returns a new Vector; `__eq__` compares the three coordinates as a tuple.

   ```python
   class Vector:
       def __init__(self, x, y, z):
           self.x, self.y, self.z = x, y, z
       def __sub__(self, other):
           return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
       def __eq__(self, other):
           return (self.x, self.y, self.z) == (other.x, other.y, other.z)
   ```

5. Task 4, `Person.age`. `self.age = age` in `__init__` already goes through the setter, so validation also happens at creation. The real value lives in `self._age`.

   ```python
   class Person:
       def __init__(self, age):
           self.age = age
       @property
       def age(self):
           return self._age
       @age.setter
       def age(self, value):
           if not 0 <= value <= 150:
               raise ValueError("age must be between 0 and 150")
           self._age = value
   ```

6. Task 5, `BankAccount`. `withdraw` returns `False` and changes nothing when the amount is too large.

   ```python
   def withdraw(self, amount):
       if amount > self.balance:
           return False
       self.balance -= amount
       return True

   def __str__(self):
       return f"{self.owner}: balance {self.balance}"
   ```

   Add `__init__(self, owner, balance=0)` and a `deposit` that does `self.balance += amount`.

7. Task 6, shapes. The base `Shape.area()` just does `raise NotImplementedError`. Each subclass stores its sizes in `__init__` and overrides `area`; `total_area` calls `area()` on each item without caring which kind it is.

   ```python
   class Rectangle(Shape):
       def area(self):
           return self.width * self.height

   class Circle(Shape):
       def area(self):
           return math.pi * self.radius ** 2

   def total_area(shapes):
       return sum(s.area() for s in shapes)
   ```

8. Task 7, library. `self.__books` is stored as `_Library__books`, so `lib.books` and `lib._books` do not exist (the check tests this). A dict keyed by ISBN makes `find` easy. `Book.__init__` just stores `title`, `isbn` and `is_available = True`.

   ```python
   class Library:
       def __init__(self):
           self.__books = {}
       def add(self, book):
           self.__books[book.isbn] = book
       def find(self, isbn):
           return self.__books.get(isbn)
       def __len__(self):
           return len(self.__books)

   class Member:
       def __init__(self, name):
           self.name = name
           self.__borrowed = set()
       def borrow(self, library, isbn):
           book = library.find(isbn)
           if book is None or not book.is_available:
               return False
           book.is_available = False
           self.__borrowed.add(isbn)
           return True
       def give_back(self, library, isbn):
           if isbn in self.__borrowed:
               library.find(isbn).is_available = True
               self.__borrowed.discard(isbn)
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Press Done for the flag.

**Common mistakes.**

- `self.count += 1` in `Item`: it creates an instance attribute and `Item.count` stays at 0.
- In the property setter, writing `self.age = value` instead of `self._age = value`, which calls the setter again forever (`RecursionError`).
- Naming the catalog `self._books` (one underscore); the check rejects it as not private.
