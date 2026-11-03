"""Python Qualification 05: references and the memory model."""
import copy
import gc
import sys
import weakref


def identity_report():
    a, b = [1, 2, 3], [1, 2, 3]
    print(id(a), id(b))
    return a is b, a == b


def shallow_trap():
    original = {"a": [1, 2]}
    dup = copy.copy(original)
    dup["a"].append(3)
    return original


def refcount_growth():
    obj = object()
    readings = [sys.getrefcount(obj)]
    alias = obj
    readings.append(sys.getrefcount(obj))
    holder = [obj]
    readings.append(sys.getrefcount(obj))
    del alias, holder
    return readings


class _Node:
    def __init__(self):
        self.peer = None


def collect_cycle():
    a, b = _Node(), _Node()
    a.peer, b.peer = b, a
    del a, b
    return gc.collect()


def track_id(obj):
    print(obj, id(obj))
    return obj, id(obj)


def int_id_changes():
    n = 1000
    before = id(n)
    n += 1
    return id(n) != before


def my_deepcopy(data):
    if isinstance(data, dict):
        return {k: my_deepcopy(v) for k, v in data.items()}
    if isinstance(data, list):
        return [my_deepcopy(v) for v in data]
    return data


class Blob:
    def __init__(self):
        self.payload = bytes(1024)
        self.other = None


def cycle_needs_gc():
    blob = Blob()
    blob.other = blob
    ref = weakref.ref(blob)
    del blob
    before = ref() is not None
    gc.collect()
    after = ref() is not None
    return before, after
