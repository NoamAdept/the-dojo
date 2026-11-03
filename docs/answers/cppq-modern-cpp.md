## Modern C++ and Optimization

*cppq-modern-cpp · medium*

**Goal.** Use C++11 to C++17 features in `tasks.h`: range-for, inline functions instead of macros, `std::optional`, `auto`, `std::variant` with `std::visit`, structured bindings and recursive `constexpr`.

**You need to know.**

- Range-based `for (auto x : v)` and `auto` type deduction.
- Why `#define SQUARE_BAD(x) ((x) * (x))` evaluates its argument twice.
- `std::optional` / `std::nullopt`; `std::variant` + `std::visit` with a generic lambda and `if constexpr`.
- `constexpr` functions can size a `std::array` at compile time.

**Walkthrough.**

1. Run `./check`. The starter already defines `SQUARE_BAD`; add `#include <sstream>` and `#include <type_traits>`.

2. Task 1, modern loop.

   ```cpp
   inline int sumRange(const std::vector<int>& v) {
       int total = 0;
       for (int x : v) total += x;
       return total;
   }
   ```

3. Task 2, macro danger. A real function evaluates `a++` once (the test checks `square(a++) == 25 && a == 6`). The macro would expand to `((a++) * (a++))`, two increments and undefined behaviour, so `macroSurprise` counts the two increments instead of calling it.

   ```cpp
   inline int square(int x) { return x * x; }
   inline int macroSurprise() {
       int a = 5;
       int before = a;
       a++;  // what SQUARE_BAD(a++) does: two increments
       a++;
       return a - before;
   }
   ```

4. Task 3, optional.

   ```cpp
   inline std::optional<std::string> getName(int id) {
       if (id == 1) return "Alice";
       return std::nullopt;
   }
   ```

5. Task 4, statistics with `auto`. `auto sum = 0.0` deduces `double`; plain `0` would deduce `int` and truncate.

   ```cpp
   inline double average(const std::vector<double>& v) {
       if (v.empty()) return 0.0;
       auto sum = 0.0;
       for (auto x : v) sum += x;
       return sum / v.size();
   }
   ```

6. Task 5, variant and visit. The lambda gets whichever type is active; `if constexpr` picks the label. An `ostringstream` prints `2.5`, while `std::to_string(2.5f)` would give `2.500000`.

   ```cpp
   using ConfigValue = std::variant<int, float, std::string>;

   inline std::string describe(const ConfigValue& v) {
       return std::visit([](const auto& x) -> std::string {
           using T = std::decay_t<decltype(x)>;
           std::ostringstream out;
           if constexpr (std::is_same_v<T, int>) out << "int:" << x;
           else if constexpr (std::is_same_v<T, float>) out << "float:" << x;
           else out << "string:" << x;
           return out.str();
       }, v);
   }
   ```

7. Task 6, config map. A `std::map` is already sorted by key; the structured binding `[key, value]` unpacks each pair. Add `;` only between items.

   ```cpp
   inline std::string dumpConfig(const std::map<std::string, ConfigValue>& cfg) {
       std::string out;
       for (const auto& [key, value] : cfg) {
           if (!out.empty()) out += ";";
           out += key + "=" + describe(value);
       }
       return out;
   }
   ```

8. Task 7, compile-time powers. The recursion ends at `exp == 0`. Because `power` is `constexpr`, `power(2, 4)` can be the array size (16).

   ```cpp
   constexpr int power(int base, int exp) { return exp == 0 ? 1 : base * power(base, exp - 1); }

   inline std::array<int, power(2, 4)> makePowersOfTwo() {
       std::array<int, power(2, 4)> a{};
       for (std::size_t i = 0; i < a.size(); ++i) a[i] = power(2, static_cast<int>(i));
       return a;
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Using `std::to_string` for the float in Task 5, giving `float:2.500000`.
- A trailing `;` at the end of the Task 6 string.
- Actually calling `SQUARE_BAD(a++)` in `macroSurprise`: it is undefined behaviour and `-Wall` warns about it. Explain the expansion instead.
