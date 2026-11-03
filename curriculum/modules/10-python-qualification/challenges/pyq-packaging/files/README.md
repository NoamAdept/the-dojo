# Project Structure and Packaging



## Module 10: Project Structure & Packaging

Professional developers organize their code well. In Python, this means:

- a strict folder structure (directory hierarchy)
- a `pyproject.toml` config file
- Virtual Environments

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Config parsing**: `project_name(path)` reads a `pyproject.toml` with `tomllib`. It returns `[project].name`. You can try it on the file we give you, `demo_project/pyproject.toml`.
2. **Import check**: `can_import(name)` tries to import the module. If the import raises `ModuleNotFoundError`, it returns `False`. Otherwise it returns `True`.
3. **Dependency check**: `is_installed(name)` checks if a module exists. It uses `importlib.util.find_spec`, so it does not import the module.
4. **Clean up**: `remove_tree(path)` deletes a folder and everything inside it (a directory tree). Use `shutil`. If the folder does not exist, do nothing.
5. **Setup script generator**: `scaffold(root, name)` creates these inside `root`:
   - `src/<name>/__init__.py`
   - `tests/`
   - `README.md` (the file must contain the name)
6. **Requirements parser**: `parse_requirements(path)` returns a list of package names. Skip blank lines and `#` comments. Remove version specifiers and other extra parts, like `==1.0.0`, `>=1.0`, `~=2.1`, `[extras]` and `; markers`.
7. **Virtual env wrapper**: Write a class `VirtualEnv(path)` with:
   - `create()`: runs `python -m venv --without-pip <path>`. Use `subprocess.run(..., check=True)`.
   - `python`: the path to the Python interpreter inside the env.
   - `run_script(script)`: runs the script and returns its stdout.
   - `install(package)`: builds the pip command. The check never calls it, because there is no network.

## Check your work

Run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
