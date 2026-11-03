# Compile and Repair a C++ Program: lesson

### Strict flags

So far you compiled with `g++ -std=c++17`. Real projects ask the compiler to do extra checks. In this module, you build every program like this:

```
g++ -std=c++17 -Wall -Wextra -Werror meter.cpp -o meter
```

| part | meaning |
|---|---|
| `g++` | the C++ compiler |
| `-std=c++17` | use the 2017 version of the C++ rules |
| `-Wall -Wextra` | warn about many likely mistakes ("W" = warning) |
| `-Werror` | treat every warning as an error, so the compiler stops on every warning |
| `meter.cpp` | the source file to compile |
| `-o meter` | name the finished program `meter` |

A **warning** is a message about code that is allowed, but is probably wrong. Here is an example:

```cpp
int main() {
    int count = 3;     // made, but never used
    return 0;
}
```

```
meter.cpp:2:9: error: unused variable 'count' [-Werror=unused-variable]
cc1plus: all warnings being treated as errors
```

Without `-Werror`, this is only a warning. The program still builds. With `-Werror`, you must fix it. Use the variable, or delete it.

### Fix from the top down

Each message starts with `file:line:column`. So `meter.cpp:2:9` means file `meter.cpp`, line 2, column 9.

Fix the **first** message. Then compile again. Later messages are often caused by the first one. When you fix the first one, they often go away too.

You will see 2 messages today:

- `expected ';' before ...`: a line is missing its `;`. The compiler only sees this at the start of the **next** line. So look 1 line up.
- `'x' was not declared in this scope`: the name was never created. Every variable needs a type the first time it appears (`double x = 1.5;`). The spelling must also match exactly.

### Operator order

In C++, `*` and `/` happen before `+` and `-`. This is the same as in school maths. This rule is called **operator precedence** (the order in which operators are done):

```cpp
double x = 2 + 4 / 2.0;      // 4.0  (4 / 2.0 first, then + 2)
double y = (2 + 4) / 2.0;    // 3.0  (brackets first)
```

Use brackets to say exactly what you mean.

There is one more trap. When both sides are whole numbers, `/` removes the fraction. For example, `7 / 2` is `3`. This is called **integer division**. When one side is a `double` (a number with a fraction part), you get the fraction. For example, `7.0 / 2` is `3.5`.

### Exactly one digit after the point

`std::cout` prints a `double` as short as it can. For example:

- `std::cout << 20.0` prints `20`.
- `std::cout << 7.0 / 3` prints `2.33333`.

You may want exactly 1 digit after the point every time. To do this, add `#include <iomanip>`. Then send 2 settings to `std::cout` before the number:

```cpp
std::cout << std::fixed << std::setprecision(1) << 20.0 << "\n";     // 20.0
std::cout << std::fixed << std::setprecision(1) << 7.0 / 3 << "\n";  // 2.3
```

- `std::fixed` means "always write digits after the point".
- `std::setprecision(1)` means "write exactly 1 of them". The last digit is rounded.

Both settings stay on. They also apply to later numbers that you print with `std::cout`.

### New words

- compiler flag: an option like `-Wall` that changes how g++ works.
- warning: a message about code that is legal but probably wrong.
- `-Werror`: makes warnings stop the build, like errors do.
- operator precedence: which operators are done first (`*` `/` before `+` `-`).
- integer division: `/` on two whole numbers. It drops the fraction.
- `double`: a number type that can hold a fraction, like 3.5.
- `std::fixed` / `std::setprecision(n)`: print a number with exactly n digits after the point.

## Offline help

- Offline: run `man g++`. Then type `/-Wextra` and press Enter. This jumps to the part about warnings.
