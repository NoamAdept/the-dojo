"""Python Qualification 05: references and the memory model."""
import copy
import gc
import sys
import weakref


def identity_report():
    raise NotImplementedError


def shallow_trap():
    raise NotImplementedError


def refcount_growth():
    raise NotImplementedError


def collect_cycle():
    raise NotImplementedError


def track_id(obj):
    raise NotImplementedError


def int_id_changes():
    raise NotImplementedError


def my_deepcopy(data):
    raise NotImplementedError


class Blob:
    def __init__(self):
        self.payload = bytes(1024)
        self.other = None


def cycle_needs_gc():
    raise NotImplementedError
