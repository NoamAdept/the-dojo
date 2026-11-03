# Modern C++ and Optimization

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

## Modern C++ & Optimization (C++11/14/17/20)

C++ has changed a lot. "Modern C++" means C++11 and newer. Its features make code safer and clearer. Compiler optimizations and keywords like `inline` make sure that it also runs fast.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **Modern loop**: `int sumRange(const std::vector<int>&)` uses a range-based for loop.
2. **Macro danger**:
   - Write `inline int square(int)`.
   - Then write `int macroSurprise()`. It shows what `SQUARE_BAD(a++)` does to `a` (start with 5).
   - It returns how many times `a` was incremented (2).
3. **Safe optional**: `std::optional<std::string> getName(int id)` returns `"Alice"` for 1. For any other id it returns `std::nullopt`.
4. **Statistics**: `double average(const std::vector<double>&)` uses `auto` and range-for. It returns 0 for an empty vector.
5. **Config variant**: write `using ConfigValue = std::variant<int, float, std::string>;` and `std::string describe(const ConfigValue&)`. Use `std::visit`. It returns `"int:3"`, `"float:2.5"` or `"string:fm"`.
6. **Config map**: `std::string dumpConfig(const std::map<std::string, ConfigValue>&)` joins `key=describe(value)` with `;`. Keep the keys in order.
7. **Compile-time powers**:
   - Write a recursive `constexpr int power(int base, int exp)`.
   - Write `std::array<int, power(2, 4)> makePowersOfTwo()`. Fill it with 2^0 to 2^15.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
