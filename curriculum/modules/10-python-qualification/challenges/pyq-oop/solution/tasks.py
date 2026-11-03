"""Python Qualification 03: classes and objects."""
import math


class Vehicle:
    def __init__(self, make, model):
        self.make, self.model = make, model

    def drive(self):
        return "Vroom"


class Item:
    count = 0

    def __init__(self):
        Item.count += 1


class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


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


class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def __str__(self):
        return f"{self.owner}: balance {self.balance}"


class Shape:
    def area(self):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


def total_area(shapes):
    return sum(s.area() for s in shapes)


class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.is_available = True


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
