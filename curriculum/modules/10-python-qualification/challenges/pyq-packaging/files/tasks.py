"""Python Qualification 10: project structure and packaging."""
import importlib
import importlib.util
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def project_name(path):
    raise NotImplementedError


def can_import(name):
    raise NotImplementedError


def is_installed(name):
    raise NotImplementedError


def remove_tree(path):
    raise NotImplementedError


def scaffold(root, name):
    raise NotImplementedError


def parse_requirements(path):
    raise NotImplementedError


class VirtualEnv:
    pass
