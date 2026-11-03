"""Python Qualification 09: error and exception handling."""
import functools


def read_int(inputs):
    raise NotImplementedError


def safe_get(lst, i):
    raise NotImplementedError


class InvalidAgeError(ValueError):
    pass


def set_age(age):
    raise NotImplementedError


def use_resource(log, fail):
    raise NotImplementedError


def safe_divide(a, b):
    raise NotImplementedError


def retry(attempts=3):
    raise NotImplementedError


class InsufficientFunds(Exception):
    pass


class InvalidAccount(Exception):
    pass


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def transfer(self, amount, target, accounts):
        raise NotImplementedError


def process_batch(batch, accounts):
    raise NotImplementedError
