# Error Handling and Safety

Write all your code in `tasks.h`. You may put all the code in the header, as inline code. Each file in `tests/` checks one task. `./check` compiles the tests one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## Error Handling and Safety

Welcome to Module 9! Things go wrong. This always happens. How you handle errors decides how robust (strong and reliable) your system is.

In C++, there are 2 main ways:
1.  **Exceptions**: the standard C++ way. Good for high-level logic.
2.  **Return Codes / Types**: used in Embedded and Real-Time systems, where exceptions cost too much.

Is this new to you? Read **LESSON.md** first, or press **Lesson** in the app.

## Your tasks

1. **Catching range errors**: write `std::string safeAt(const std::vector<int>&, std::size_t i)`. It uses `.at(i)`. If it catches the exception, it returns `"out_of_range"`. Otherwise it returns the number as text.
2. **Nodiscard**: write `[[nodiscard]] int square(int)`. The test compiles a call that ignores the result, with `-Werror`. It expects this compile to fail.
3. **Optional parser**: write `std::optional<int> parsePositive(int)`.
4. **Safe division**: write `std::optional<float> safeDivide(float, float)`.
5. **Custom exception**: write `SensorException : std::exception`. You build it from a sensor id. Its `what()` returns `"sensor <id> failed"`. Then write `int readSensor(int id)`. For a negative id, it throws the exception. Otherwise it returns `id * 10`.
6. **Result type**: write `template <class T, class E> class Result`. It holds a `std::variant<T, E>`. It has:
   - static `ok(T)` and `err(E)`
   - `isOk()`
   - `value()` and `error()`
7. **File loader**: write `enum class LoadError { NotFound, Denied };` and `Result<std::string, LoadError> loadFile(const std::string& name)`. The rules are:
   - `"secret.cfg"` gives Denied.
   - A name that does not start with `"data/"` gives NotFound.
   - Any other name returns `"contents of <name>"`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
