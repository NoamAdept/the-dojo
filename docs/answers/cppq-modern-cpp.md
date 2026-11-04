# Modern Channel Scanner

`cppq-modern-cpp` · Orange Belt

**Goal:** Use C++11 to C++17 features in `tasks.h`: range-for, inline functions instead of macros, `std::optional`, `auto`, `std::variant` with `std::visit`, structured bindings and recursive `constexpr`.

**File `tasks.h`**

```cpp
#pragma once
#include <array>
#include <map>
#include <optional>
#include <sstream>
#include <string>
#include <type_traits>
#include <variant>
#include <vector>

#define SQUARE_BAD(x) ((x) * (x))

inline int sumRange(const std::vector<int>& v) {
    int total = 0;
    for (int x : v) total += x;
    return total;
}

inline int square(int x) { return x * x; }

inline int macroSurprise() {
    int a = 5;
    int before = a;
    a++;
    a++;
    return a - before;
}

inline std::optional<std::string> getName(int id) {
    if (id == 1) return "Alice";
    return std::nullopt;
}

inline double average(const std::vector<double>& v) {
    if (v.empty()) return 0.0;
    auto sum = 0.0;
    for (auto x : v) sum += x;
    return sum / v.size();
}

using ConfigValue = std::variant<int, float, std::string>;

inline std::string describe(const ConfigValue& v) {
    return std::visit(
        [](const auto& x) -> std::string {
            using T = std::decay_t<decltype(x)>;
            std::ostringstream out;
            if constexpr (std::is_same_v<T, int>) out << "int:" << x;
            else if constexpr (std::is_same_v<T, float>) out << "float:" << x;
            else out << "string:" << x;
            return out.str();
        },
        v);
}

inline std::string dumpConfig(const std::map<std::string, ConfigValue>& cfg) {
    std::string out;
    for (const auto& [key, value] : cfg) {
        if (!out.empty()) out += ";";
        out += key + "=" + describe(value);
    }
    return out;
}

constexpr int power(int base, int exp) { return exp == 0 ? 1 : base * power(base, exp - 1); }

inline std::array<int, power(2, 4)> makePowersOfTwo() {
    std::array<int, power(2, 4)> a{};
    for (std::size_t i = 0; i < a.size(); ++i) a[i] = power(2, static_cast<int>(i));
    return a;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
