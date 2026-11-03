#!/usr/bin/env python3
"""Run with ./check. Tests each task in tasks.py and lists what still fails."""
import sys
sys.path.insert(0, ".")
sys.dont_write_bytecode = True
failed, passed = [], []

def task(name):
    def run(fn):
        try:
            fn()
            passed.append(name)
        except NotImplementedError:
            failed.append(f"{name}: not implemented yet")
        except Exception as exc:  # show the learner what broke
            failed.append(f"{name}: {exc}" if isinstance(exc, AssertionError) and str(exc) else f"{name}: {type(exc).__name__}: {exc}")
        return fn
    return run

import math, tasks

@task("1 Vehicle")
def _():
    v = tasks.Vehicle("Raspberry", "Pi 5")
    assert (v.make, v.model) == ("Raspberry", "Pi 5") and v.drive() == "Vroom"

@task("2 Item counter")
def _():
    start = tasks.Item.count
    for _ in range(3):
        tasks.Item()
    assert tasks.Item.count == start + 3

@task("3 Vector subtraction")
def _():
    d = tasks.Vector(5, 7, 9) - tasks.Vector(1, 2, 3)
    assert isinstance(d, tasks.Vector) and d == tasks.Vector(4, 5, 6)

@task("4 Person.age property")
def _():
    p = tasks.Person(30)
    p.age = 150
    for bad in (-1, 151):
        try:
            p.age = bad
        except ValueError:
            pass
        else:
            raise AssertionError(f"age={bad} should raise ValueError")
    assert p.age == 150

@task("5 BankAccount")
def _():
    a = tasks.BankAccount("noam", 100)
    a.deposit(50)
    assert a.withdraw(500) is False and a.balance == 150
    assert a.withdraw(20) is True and a.balance == 130
    assert "noam" in str(a) and "130" in str(a)

@task("6 Shape polymorphism")
def _():
    try:
        tasks.Shape().area()
    except NotImplementedError:
        pass
    else:
        raise AssertionError("Shape().area() must raise NotImplementedError")
    assert tasks.Rectangle(2, 3).area() == 6
    assert abs(tasks.Circle(1).area() - math.pi) < 1e-9
    assert abs(tasks.total_area([tasks.Rectangle(2, 3), tasks.Circle(1)]) - (6 + math.pi)) < 1e-9

@task("7 Library system")
def _():
    lib = tasks.Library()
    lib.add(tasks.Book("Think Python", "111"))
    lib.add(tasks.Book("DSP Guide", "222"))
    assert len(lib) == 2 and lib.find("111").title == "Think Python"
    assert not hasattr(lib, "books") and not hasattr(lib, "_books"), "keep the catalog private (self.__books)"
    a, b = tasks.Member("a"), tasks.Member("b")
    assert a.borrow(lib, "111") is True and lib.find("111").is_available is False
    assert b.borrow(lib, "111") is False
    a.give_back(lib, "111")
    assert lib.find("111").is_available and b.borrow(lib, "111") is True

print(f"{len(passed)}/{len(passed) + len(failed)} tasks pass")
if failed:
    print("Not yet:")
    for line in failed:
        print("  -", line)
    raise SystemExit(1)
print("CHECK_OK")
