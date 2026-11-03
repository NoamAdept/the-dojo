# Modern C++ and Optimization: lesson

### 1. Type Inference (`auto`)

With `auto`, the compiler finds out (deduces) the type for you. This stops type mismatches (using the wrong type). It also makes the code cleaner.

```cpp
#include <iostream>
#include <vector>

int main() {
    auto a = 10;        // int
    auto b = 3.14;      // double
    
    std::vector<int> numbers = {1, 2, 3};
    // Instead of std::vector<int>::iterator it = ...
    auto it = numbers.begin();
    
    std::cout << "a: " << a << ", b: " << b << std::endl;
    return 0;
}
```

### 2. Range-based `for` loops

A range-based `for` loop goes through each element of a container or array. You do not need to count with an index.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {10, 20, 30};
    
    for (const auto& n : numbers) {
        std::cout << n << " ";
    }
    std::cout << std::endl;
    return 0;
}
```

### 3. `nullptr`

`NULL` is just `0` (an int). `nullptr` has its own type (`std::nullptr_t`) and is only for pointers. So the compiler never confuses it with a number.

### 4. Scoped Enums (`enum class`)

Old C-style enums put all their names in the global namespace. This can cause name clashes. An `enum class` is strongly typed (it does not turn into an int by itself). Its names stay inside its own scope.

```cpp
#include <iostream>

enum class Color { Red, Green, Blue };

int main() {
    Color c = Color::Red;
    if (c == Color::Red) {
        std::cout << "It is Red" << std::endl;
    }
    return 0;
}
```

### 5. `constexpr` (Compile-Time Math)

With `constexpr`, the compiler calculates values during **compilation**, not when the program runs. This saves CPU time on the embedded device. The values can also be stored in Read-Only Memory (Flash).

```cpp
#include <iostream>

constexpr int fib(int n) {
    return (n <= 1) ? n : fib(n-1) + fib(n-2);
}

int main() {
    // Calculated by compiler!
    constexpr int val = fib(10);
    
    std::cout << "Fib(10): " << val << std::endl;
    return 0;
}
```

### 6. `inline` Functions

`inline` is a suggestion to the compiler. It says: *"Don't call this function. Copy-paste its body right here."* This removes the cost of a function call for small functions. (A call has to push data onto the stack and pop it off again.)

**VS Macros**: `inline` is type-safe, and you can debug it. Macros (`#define`) are dangerous. They only replace text.

```cpp
#include <iostream>

// Suggest inlining
inline int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 10);
    // Compiler likely converts this to: int result = 5 + 10;
    std::cout << "Result: " << result << std::endl;
    return 0;
}
```

### 7. `std::array` (C++11)

`std::array` replaces C-style arrays (`int arr[5]`). It is safer and has zero overhead (it is not slower). It knows its own size.

### 8. Structured Binding (C++17)

Structured binding unpacks tuples, pairs, or structs into separate variables in one clean line.

```cpp
#include <iostream>
#include <tuple>

struct Entry {
    int id;
    std::string name;
};

int main() {
    Entry e{1, "Admin"};
    auto [id, name] = e;
    std::cout << "ID: " << id << ", Name: " << name << std::endl;
    return 0;
}
```

### 9. `std::optional` & `std::variant` (C++17)

- `std::optional`: says that a value might be missing. This is better than returning a "magic" value like '-1'.
- `std::variant`: a type-safe union. This is better than a raw `union`.

### 10. Benchmarking (`std::chrono`)

Benchmarking means measuring how fast code runs. To measure time, we use the `<chrono>` library.

```cpp
#include <iostream>
#include <chrono>

void heavyWork() {
    volatile int temp = 0;
    for(int i=0; i<1000000; ++i) temp += i;
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();
    heavyWork();
    auto end = std::chrono::high_resolution_clock::now();
    
    std::chrono::duration<double> diff = end - start;
    std::cout << "Time: " << diff.count() << "s" << std::endl;
    return 0;
}
```

---

## New words

- **deduce**: find out from the code. The compiler deduces the type for `auto`.
- **compile time**: when the compiler builds your program. **Run time** is when the program runs.
- **macro**: a `#define` rule that replaces text before compiling.
- **overhead**: extra work or time that a feature costs.
- **type-safe**: the compiler stops you from using the wrong type.
