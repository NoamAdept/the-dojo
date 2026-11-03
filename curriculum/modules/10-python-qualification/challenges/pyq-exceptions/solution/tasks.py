"""Python Qualification 09: error and exception handling."""
import functools


def read_int(inputs):
    for text in inputs:
        try:
            return int(text)
        except ValueError:
            print("Invalid")


def safe_get(lst, i):
    try:
        return lst[i]
    except IndexError:
        return None


class InvalidAgeError(ValueError):
    pass


def set_age(age):
    if not 0 <= age <= 150:
        raise InvalidAgeError(f"age out of range: {age}")
    return age


def use_resource(log, fail):
    log.append("open")
    try:
        if fail:
            raise RuntimeError("resource failure")
    finally:
        log.append("closed")


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float("inf")
    except TypeError:
        print("Inputs must be numbers")
        return None


def retry(attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == attempts:
                        raise
                    print("Retrying...")
        return wrapper
    return decorator


class InsufficientFunds(Exception):
    pass


class InvalidAccount(Exception):
    pass


class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def transfer(self, amount, target, accounts):
        if target not in accounts:
            raise InvalidAccount(target)
        if amount > self.balance:
            raise InsufficientFunds(f"{self.name} has {self.balance}, needs {amount}")
        self.balance -= amount
        accounts[target].balance += amount


def process_batch(batch, accounts):
    done, errors = 0, []
    for source, target, amount in batch:
        try:
            accounts[source].transfer(amount, target, accounts)
            done += 1
        except (InsufficientFunds, InvalidAccount) as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
    return done, errors
