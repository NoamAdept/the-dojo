# Classes and Objects



## Module 3: Classes and Objects (OOP)

Python lets you program in several styles (it is multi-paradigm). But at its core, it is object-oriented. In Python, everything is an object: functions, modules and basic types too. In this module, you learn how to define your own types.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Write these classes in `tasks.py`.

1. **Vehicle**: `Vehicle(make, model)` has a method `drive()` that returns `"Vroom"`.
2. **Static counter**: `Item` counts how many objects you created. It keeps the number in the class attribute `Item.count`.
3. **Vector math**: `Vector(x, y, z)` supports `a - b` (it returns a new Vector) and `==`.
4. **Validated attribute**: `Person(age)` has an `age` property. It raises `ValueError` for values below 0 or above 150.
5. **Bank account**: `BankAccount(owner, balance=0)` has `deposit(amount)` and `withdraw(amount)`.
   - If a withdrawal is larger than the balance, it returns `False` and does not change the balance.
   - Otherwise it returns `True`.
   - `str(acct)` contains the owner and the balance.
6. **Shape polymorphism**: the base method `Shape.area()` raises `NotImplementedError`. `Rectangle(w, h)` and `Circle(r)` implement it. `total_area(shapes)` adds up all the areas.
7. **Library system**:
   - `Book(title, isbn)` has `is_available`.
   - `Library` keeps its books private (`self.__books`). It has `add(book)`, `find(isbn)` and `len(library)`.
   - `Member(name)` has `borrow(library, isbn)` and `give_back(library, isbn)`.
   - If a book is not available, borrowing it returns `False`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
