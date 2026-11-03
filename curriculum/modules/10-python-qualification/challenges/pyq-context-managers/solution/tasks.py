"""Python Qualification 08: resource management and context managers."""
import functools
import os
import tempfile
import time
from contextlib import contextmanager


def write_numbers(path):
    with open(path, "w") as fh:
        for i in range(1, 11):
            fh.write(f"{i}\n")


@contextmanager
def html_tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:
        print(f"</{name}>")


class ExceptionSpy:
    def __init__(self):
        self.seen = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.seen = True
            print("An error occurred!")
        return False


def temp_dir_lifecycle():
    with tempfile.TemporaryDirectory() as path:
        inside = os.path.isdir(path)
        print(path)
    return inside, os.path.exists(path)


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self.start
        return False


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with Timer() as t:
            result = func(*args, **kwargs)
        wrapper.last_elapsed = t.elapsed
        return result
    return wrapper


class Cursor:
    def execute(self, sql):
        return f"ran: {sql}"


class DatabaseConnection:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("connect")
        return Cursor()

    def __exit__(self, exc_type, exc, tb):
        self.log.append("rollback" if exc_type else "commit")
        self.log.append("disconnect")
        return False


LEVEL = 0


class Indenter:
    def __enter__(self):
        global LEVEL
        LEVEL += 1
        return self

    def __exit__(self, *exc):
        global LEVEL
        LEVEL -= 1
        return False


def indented(msg):
    return "    " * LEVEL + msg
