"""Python Qualification 12: dataclasses and serialization."""
import functools
import json
import os
import pickle
from dataclasses import asdict, dataclass


# Task 1: Item dataclass


def student_json():
    raise NotImplementedError


def pickle_roundtrip(obj):
    raise NotImplementedError


# Task 4: frozen Settings dataclass


def save_config(config, filename):
    raise NotImplementedError


def load_config(filename):
    raise NotImplementedError


# Task 6: User dataclass


def serialize_users(users, filename):
    raise NotImplementedError


def deserialize_users(filename):
    raise NotImplementedError


def file_cache(filename):
    raise NotImplementedError
