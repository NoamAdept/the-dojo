# Reading and Writing Files

**What you will learn:** how a Python program reads a text file and writes a new one.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Replace each `raise NotImplementedError` in `tasks.py`. You can try your functions on `notes.txt` at the `>>>` prompt. First type `import tasks`, then `tasks.read_all("notes.txt")`.

1. **read_all**: `read_all(path)` returns the whole file as one string.
2. **count_lines**: `count_lines(path)` returns how many lines the file has. Count them in a `for` loop over the file.
3. **read_lines**: `read_lines(path)` returns a list of the file's lines, with `strip()` used on each one. Leave out blank lines and lines that start with `#`.
4. **write_lines**: `write_lines(path, lines)` writes each string in the list `lines` to the file, each on its own line. Add the `"\n"`.
5. **shout_file**: `shout_file(src, dst)` does 3 things:
   - It reads the lines of `src` with your `read_lines`.
   - It makes each line upper case.
   - It writes them to `dst` with your `write_lines`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
