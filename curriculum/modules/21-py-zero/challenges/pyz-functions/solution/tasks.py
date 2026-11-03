"""Python from Zero 03: functions."""


def double(n):
    return n * 2


def greet(name):
    return f"Hello, {name}!"


def area(width, height):
    return width * height


def to_khz(hz):
    return hz / 1000


def average(a, b):
    return (a + b) / 2


def quadruple(n):
    return double(double(n))
