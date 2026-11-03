# Error Handling and Safety: lesson

### 1. Exceptions: Basic Syntax

An exception is a way to signal an error. Some code *must* handle the error. If nothing handles it, the program crashes.

```cpp
#include <iostream>
#include <stdexcept>

int divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero!");
    }
    return a / b;
}

int main() {
    try {
        divide(10, 0);
    } catch (const std::exception& e) {
        std::cout << "Exception caught: " << e.what() << std::endl;
    }
    return 0;
}
```

### 2. Standard Exceptions

Always use the standard types from `<stdexcept>`:
- `std::runtime_error`
- `std::logic_error`
- `std::out_of_range`
- `std::invalid_argument`

### 3. Stack Unwinding (RAII + Exceptions)

When code throws an exception, C++ "unwinds" the stack. This means it leaves each function in turn. On the way, it calls the **destructors** of all local objects. So you get no memory leaks, **IF** you use RAII (Smart Pointers, Vectors, and so on).

```cpp
#include <iostream>

class Worker {
public:
    Worker() { std::cout << "Worker construct" << std::endl; }
    ~Worker() { std::cout << "Worker destruct" << std::endl; }
};

int main() {
    try {
        Worker w;
        throw "Boom";
    } catch (...) {
        std::cout << "Caught exception" << std::endl;
    }
    return 0;
}
```

### 4. `noexcept` Keyword

Some functions promise that they will **never** throw. Mark these functions `noexcept`. Then the compiler can optimize more.
If a `noexcept` function *does* throw, the program stops at once.

### 5. When NOT to use Exceptions (Embedded Systems)

Many embedded systems turn exceptions off (`-fno-exceptions`). The Google C++ Style does this too. The reasons are:
1.  **Code Size**: exception tables use up flash memory.
2.  **Determinism**: you cannot predict how long unwinding takes. This is bad for Real-Time systems, which must always respond in time.
3.  **Heap**: some implementations use heap memory (memory reserved while the program runs).

In these cases, we use **Return Values** instead.

### 6. Return Codes & `[[nodiscard]]`

Return an enum that says what happened (the status). Add `[[nodiscard]]` (C++17). Then the compiler warns if the caller does not check the result.

```cpp
#include <iostream>

enum class Status { Success, Error };

[[nodiscard]] Status initSensor() {
    return Status::Error;
}

int main() {
    // initSensor(); // Warning: Ignoring return value!
    if (initSensor() != Status::Success) {
        std::cout << "Sensor Failed" << std::endl;
    }
    return 0;
}
```

### 7. `std::optional` (Value or Nothing)

Use this for functions that return data but might fail. It does not say why it failed (there is no error code).

```cpp
#include <iostream>
#include <optional>

std::optional<int> findUser(int id) {
    if (id == 1) return 42;
    return std::nullopt;
}

int main() {
    if (auto user = findUser(99)) {
        std::cout << "User ID: " << *user << std::endl;
    } else {
        std::cout << "User not found" << std::endl;
    }
    return 0;
}
```

### 8. `std::expected` (C++23) / Result Pattern

This is the best choice. It returns **Either** a valid Value **Or** an Error Code. (It is like `Result` in Rust.)
In C++17 we can copy this idea with `std::variant<Value, Error>`.

---

## New words

- **exception**: an object you throw to signal an error.
- **stack unwinding**: leaving functions one by one after a throw, and calling destructors on the way.
- **deterministic**: always takes a time (or gives a result) you can predict.
- **heap**: memory the program reserves while it runs.
- **return code**: a value a function returns to say if it worked.
- **optional**: a value that may or may not be there.
