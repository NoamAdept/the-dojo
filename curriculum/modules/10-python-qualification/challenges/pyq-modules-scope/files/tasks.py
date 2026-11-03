"""Python Qualification 01: modules, packages and namespaces."""

score = 0
REGISTRY = {}


def factorial_of_ten():
    """Task 1: return 10! using the math module."""
    raise NotImplementedError


def current_dir():
    """Task 2: import os as operating_system and return getcwd()."""
    raise NotImplementedError


def increment():
    """Task 3: add 1 to the module-level score (use `global`)."""
    raise NotImplementedError


def maker(n):
    """Task 4: return a function inner(x) that returns x + n."""
    raise NotImplementedError


def calc_demo():
    """Task 5: import simple_calc and return (add(2, 3), sub(10, 4))."""
    raise NotImplementedError


def register(func):
    """Task 7: store func in REGISTRY under func.__name__, return func."""
    raise NotImplementedError


# Task 7: decorate three functions with @register here.


def run_all():
    """Task 7: call every registered function; return {name: result}."""
    raise NotImplementedError
