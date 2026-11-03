## Project Structure and Packaging

*pyq-packaging · medium*

**Goal.** Write helpers in `tasks.py` that read `pyproject.toml`, test whether modules exist, clean up and scaffold a project, parse `requirements.txt`, and drive a virtual environment with `subprocess`.

**You need to know.**

- `tomllib` (Python 3.11+) reads TOML from a file opened in binary mode.
- `importlib.import_module` vs `importlib.util.find_spec` (find without importing).
- `shutil.rmtree` and `pathlib.Path` (`mkdir`, `touch`, `write_text`).
- `python -m venv` and `subprocess.run([...], check=True, capture_output=True, text=True)`.

**Walkthrough.**

1. Run `./check` and look at the sample config.

   ```bash
   ./check
   cat demo_project/pyproject.toml
   ```

2. Task 1. Open in `"rb"` because `tomllib.load` wants bytes, then index into the `[project]` table.

   ```python
   def project_name(path):
       with open(path, "rb") as fh:
           return tomllib.load(fh)["project"]["name"]
   ```

3. Task 2. Try the import and catch only `ModuleNotFoundError`.

   ```python
   def can_import(name):
       try:
           importlib.import_module(name)
           return True
       except ModuleNotFoundError:
           return False
   ```

4. Task 3. `find_spec` returns `None` for a missing module and never runs its code.

   ```python
   def is_installed(name):
       return importlib.util.find_spec(name) is not None
   ```

5. Task 4. `ignore_errors=True` makes a second call on a missing folder a no-op.

   ```python
   def remove_tree(path):
       shutil.rmtree(path, ignore_errors=True)
   ```

6. Task 5. `parents=True` creates `src/` and `src/<name>/` in one go; `exist_ok=True` makes it safe to run twice.

   ```python
   def scaffold(root, name):
       root = Path(root)
       (root / "src" / name).mkdir(parents=True, exist_ok=True)
       (root / "src" / name / "__init__.py").touch()
       (root / "tests").mkdir(exist_ok=True)
       (root / "README.md").write_text(f"# {name}\n")
   ```

7. Task 6. Add `import re` at the top. Drop anything after `#`, skip blank lines, and keep only the leading run of name characters, which stops at `=`, `>`, `~`, `[`, space or `;`.

   ```python
   def parse_requirements(path):
       names = []
       for line in Path(path).read_text().splitlines():
           line = line.split("#", 1)[0].strip()
           if line:
               names.append(re.match(r"[A-Za-z0-9._-]+", line).group(0))
       return names
   ```

8. Task 7. Pass commands as lists (no shell). `--without-pip` keeps creation fast and offline. The env's interpreter is `<path>/bin/python` on Linux.

   ```python
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
   ```

   The check never calls `install`, because there is no network and the env has no pip.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. Task 7 creates a real venv in a temp folder, so it takes a few seconds on a Pi. Press Done for the flag.

**Common mistakes.**

- Opening `pyproject.toml` with `"r"`; `tomllib.load` raises `TypeError` and wants a binary file.
- Splitting requirements on `==` only, so `scipy>=1.10` and `requests[socks]~=2.31 ; ...` come out wrong.
- Using `subprocess.run("python -m venv ...", shell=True)` or forgetting `capture_output=True, text=True`, so `run_script` returns `None` instead of the printed text.
