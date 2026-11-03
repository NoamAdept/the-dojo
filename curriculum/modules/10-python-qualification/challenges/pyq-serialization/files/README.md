# Dataclasses and Serialization



## Module 12: Dataclasses & Serialization

Programs often need to save data (persistence) and send data to other programs (exchange). To do this, you change objects in memory into formats like JSON or bytes. Then you can store them or send them over a network. Python makes this easy with:

- `dataclasses` (like C structs, but with many extra features)
- strong modules in the standard library

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Dataclass init**: `@dataclass Item(name: str, price: float)`.
2. **JSON dump**: `student_json()` returns this data as a JSON string: `{"name": "John", "grades": [80, 90]}`.
3. **Pickle round trip**: `pickle_roundtrip(obj)` returns `(data_bytes, restored_obj)`.
4. **Immutable dataclass**: Write a frozen `Settings(debug: bool)`. If you try to set `debug`, Python raises `dataclasses.FrozenInstanceError`.
5. **Config saver**: Write `save_config(config, filename)` and `load_config(filename)`. Use JSON.
6. **Dataclass serializer**: `@dataclass User(name: str, age: int)`. `serialize_users(users, filename)` writes the users as JSON. Use `asdict`. `deserialize_users(filename)` reads the file and builds the `User` list again.
7. **Smart cache**: `file_cache(filename)` is a decorator for a function with 1 argument. It saves the results in `filename`, as a pickled dict `{arg: result}`. So on a second call with the same argument, the function does not run again. This is true even after the module is loaded again.

## Check your work

Run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
