"""Python Qualification 01: modules, packages and namespaces."""

score = 0
REGISTRY = {}


def factorial_of_ten():
    import math
    return math.factorial(10)


def current_dir():
    import os as operating_system
    return operating_system.getcwd()


def increment():
    global score
    score += 1


def maker(n):
    def inner(x):
        return x + n
    return inner


def calc_demo():
    from simple_calc import add, sub
    return add(2, 3), sub(10, 4)


def register(func):
    REGISTRY[func.__name__] = func
    return func


@register
def hello():
    return "hello"


@register
def answer():
    return 42


@register
def pi_ish():
    return 3.14


def run_all():
    return {name: func() for name, func in REGISTRY.items()}
