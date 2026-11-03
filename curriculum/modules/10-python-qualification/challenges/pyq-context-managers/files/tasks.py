"""Python Qualification 08: resource management and context managers."""
import tempfile
import time
from contextlib import contextmanager


def write_numbers(path):
    raise NotImplementedError


@contextmanager
def html_tag(name):
    raise NotImplementedError
    yield


class ExceptionSpy:
    pass


def temp_dir_lifecycle():
    raise NotImplementedError


class Timer:
    pass


def time_it(func):
    raise NotImplementedError


class Cursor:
    def execute(self, sql):
        return f"ran: {sql}"


class DatabaseConnection:
    def __init__(self, log):
        self.log = log


LEVEL = 0


class Indenter:
    pass


def indented(msg):
    raise NotImplementedError
