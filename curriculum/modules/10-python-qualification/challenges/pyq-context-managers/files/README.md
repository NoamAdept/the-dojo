# Resource Management and Context Managers



## Module 8: Resource Management & Context Managers

In C++, RAII (Resource Acquisition Is Initialization) is the best and most common way to manage resources. Python has a pattern that does the same job: the **Context Manager**, used with the `with` statement.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **File writer**: `write_numbers(path)` uses `with open(...)` to write the numbers 1 to 10. Write 1 number on each line.
2. **Custom tagger**: `html_tag(name)` is a `@contextmanager`. It prints `<name>` on enter and `</name>` on exit. It prints `</name>` even if the body raises an exception.
3. **Exception spy**: `ExceptionSpy` is a context manager written as a class. When the body raises an exception, it:
   - sets `self.seen = True`,
   - prints `"An error occurred!"`,
   - raises the exception again (`__exit__` returns `False`).
4. **Temp dir**: `temp_dir_lifecycle()` uses `tempfile.TemporaryDirectory()`. It returns `(existed_inside, exists_after)`. The result should be `(True, False)`.
5. **Timer + time_it**: `Timer` is a context manager that stores `elapsed` seconds. `time_it` is a decorator. It runs the function inside a `Timer` and saves the time on `wrapper.last_elapsed`.
6. **Database mock**: `DatabaseConnection(log)` is a fake database connection.
   - On enter, it appends `"connect"` and returns a `Cursor`.
   - On exit, it appends `"rollback"` if an exception happened. Otherwise it appends `"commit"`.
   - Then it always appends `"disconnect"`.
   - It does not swallow (hide) the exception.
7. **Indenter**: `Indenter` adds 1 to the global indent level on enter. It subtracts 1 on exit. `indented(msg)` returns the message with 4 spaces in front for each level.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
