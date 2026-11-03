"""Python Qualification 10: project structure and packaging."""
import importlib
import importlib.util
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


def project_name(path):
    with open(path, "rb") as fh:
        return tomllib.load(fh)["project"]["name"]


def can_import(name):
    try:
        importlib.import_module(name)
        return True
    except ModuleNotFoundError:
        return False


def is_installed(name):
    return importlib.util.find_spec(name) is not None


def remove_tree(path):
    shutil.rmtree(path, ignore_errors=True)


def scaffold(root, name):
    root = Path(root)
    (root / "src" / name).mkdir(parents=True, exist_ok=True)
    (root / "src" / name / "__init__.py").touch()
    (root / "tests").mkdir(exist_ok=True)
    (root / "README.md").write_text(f"# {name}\n")


def parse_requirements(path):
    names = []
    for line in Path(path).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.append(re.match(r"[A-Za-z0-9._-]+", line).group(0))
    return names


class VirtualEnv:
    def __init__(self, path):
        self.path = Path(path)
        self.python = str(self.path / "bin" / "python")

    def create(self):
        subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(self.path)], check=True)

    def install(self, package):
        return subprocess.run([self.python, "-m", "pip", "install", package], check=True)

    def run_script(self, script):
        done = subprocess.run([self.python, str(script)], check=True, capture_output=True, text=True)
        return done.stdout
