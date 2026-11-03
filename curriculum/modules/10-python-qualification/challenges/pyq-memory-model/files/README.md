# References and the Memory Model



## Module 5: References and Memory Model

A professional Python developer must understand Python's memory model. Python allocates memory for you automatically. But you should still know *how* it does this. Then you can avoid resource leaks (memory that is never freed) and hidden bugs.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Identity inspector**: `identity_report()` makes 2 lists with the same content. It returns `(a is b, a == b)`.
2. **Shallow trap**: `shallow_trap()` does 3 steps:
   - It makes a shallow copy of `{'a': [1, 2]}`.
   - It appends `3` to the list inside the copy.
   - It returns the original dict. (The original also changed.)
3. **Ref count detective**: `refcount_growth()` returns a list of 3 `sys.getrefcount` readings for 1 object. Take the readings:
   - after you create the object,
   - after you assign it to a second name,
   - after you put it in a list.

   Each reading should be larger than the one before.
4. **Forced GC**: `collect_cycle()` builds 2 objects that reference each other. It deletes the names. It returns `gc.collect()` (more than 0).
5. **Object ID tracker**: `track_id(obj)` returns `(obj, id(obj))`. `int_id_changes()` shows that `n += 1` points the name at a new object (it rebinds the name). It returns `True`.
6. **Custom deep copy**: `my_deepcopy(data)` copies dicts and lists recursively. It leaves other values as they are.
7. **Leak simulator**: `cycle_needs_gc()` does these steps:
   - It creates a `Blob` (holding `bytes(1024)`) that references itself.
   - It keeps a `weakref.ref` to it.
   - It deletes the name.

   Return `(alive_before_gc, alive_after_gc)`. The test turns GC off while it runs. So the result should be `(True, False)`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
