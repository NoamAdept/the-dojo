# Const and Volatile Qualifiers: lesson

### 1. `const` Variables

This is the simplest use. You define a variable that nobody can change after initialization. This is safer than `#define` macros, because a `const` variable has a type and a scope.

```cpp
#include <iostream>

int main() {
    const int MAX_USERS = 100;
    
    // MAX_USERS = 101; // Compile Error: assignment of read-only variable
    
    std::cout << "Max users: " << MAX_USERS << std::endl;
    return 0;
}
```

### 2. `const` Pointers

Pointers with `const` can be confusing. Read the declaration from **Right to Left**. Then you can see which part is constant.
- `const int* p`: a pointer to a **constant int**. You cannot change the value `*p`. But you can move the pointer `p` to point somewhere else.
- `int* const p`: a **constant pointer** to an int. You can change the value `*p`. But you cannot move the pointer `p`.
- `const int* const p`: both the left and the right are const. Everything is **Frozen**. You cannot change the value, and you cannot move the pointer.

```cpp
#include <iostream>

int main() {
    int a = 10;
    int b = 20;
    
    // 1. Pointer to const int (Read-only view)
    const int* p1 = &a;
    // *p1 = 15; // Error: Can't change value
    p1 = &b;     // OK: Can change where it points
    
    // 2. Const pointer to int (Fixed arrow)
    int* const p2 = &a;
    *p2 = 15;    // OK: Can change value (a becomes 15)
    // p2 = &b;  // Error: Can't change where it points
    
    std::cout << "a is now: " << a << std::endl;
    return 0;
}
```

### 3. `const` References

This is probably the most common use in C++. When you pass a large object to a function, you pass it by reference. This avoids a copy. You add `const` so that the function cannot change your object by mistake.

**Rule of Thumb** (a simple rule that is usually right): for complex types, prefer `const T&` over `T`.

```cpp
#include <iostream>
#include <string>

// Efficient and Safe: No copy, no modification allowed
void printMessage(const std::string& msg) {
    std::cout << "Message: " << msg << std::endl;
    // msg += "!"; // Error: const reference
}

int main() {
    std::string s = "Hello World";
    printMessage(s);
    return 0;
}
```

### 4. `const` Member Functions

You can put `const` at the end of a method signature. This is a promise: the method **will not change any member variables** of the class. Because of this promise, you can call the method on `const` objects.

```cpp
#include <iostream>

class Circle {
    double radius;
public:
    Circle(double r) : radius(r) {}
    
    // This method is read-only
    double getArea() const {
        return 3.14159 * radius * radius;
    }
    
    void setRadius(double r) {
        radius = r; // Modifies state, cannot be const
    }
};

int main() {
    const Circle c(5.0); // Constant object
    
    std::cout << "Area: " << c.getArea() << std::endl; // OK: getArea is const
    
    // c.setRadius(10.0); // Error: setRadius is not const and c is const
    return 0;
}
```

### 5. `mutable` Keyword

Sometimes a method is const "logically": it does not change what the object means. But it still needs to change something inside. Examples are a mutex lock, a debug counter, or a cached (saved) calculation.

`mutable` lets you change one chosen member variable, even inside a `const` method.

```cpp
#include <iostream>

class Logger {
    mutable int accessCount = 0;
public:
    // Log is logically const (doesn't change logger configuration), but updates stats
    void log(const char* msg) const {
        std::cout << "Log: " << msg << std::endl;
        accessCount++; // OK because it is mutable
    }
    
    int getCount() const { return accessCount; }
};

int main() {
    const Logger l;
    l.log("System Start");
    std::cout << "Count: " << l.getCount() << std::endl;
    return 0;
}
```

### 6. `volatile` Keyword

This tells the compiler: *"Do not optimize reads or writes to this variable. Something outside your control might change it."*

You use it most often in embedded systems for:
- **Hardware Registers** (memory-mapped IO: hardware that you read and write like memory)
- variables in shared memory

It stops the compiler from keeping a copy of the value in a CPU register.

```cpp
#include <iostream>

// Imagine this address is mapped to a hardware button
volatile int hardware_flag = 0;

void wait_for_hardware() {
    // If 'volatile' was missing, the compiler might optimize this to 'while(true)' 
    // because it sees no code inside the loop that changes hardware_flag.
    while (hardware_flag == 0) {
        // Busy wait for external signal...
        if (hardware_flag == 1) break; // Break for demo purposes 
    }
}

int main() {
    // Simulate hardware interrupt
    hardware_flag = 1;
    wait_for_hardware();
    std::cout << "Hardware ready!" << std::endl;
    return 0;
}
```

### 7. Casting away `const` (`const_cast`)

Sometimes you must use old (legacy) APIs that do not use `const` correctly. C++ lets you remove `const` with `const_cast<T>`.

**DANGER**: if the original object was really const, changing it is Undefined Behavior. (Undefined Behavior means the C++ rules do not say what happens. Anything can happen.)

```cpp
#include <iostream>

void legacyPrint(char* str) {
    std::cout << "Legacy: " << str << std::endl;
}

int main() {
    const char* message = "Hello";
    
    // legacyPrint(message); // Error: const mismatch
    
    // We promise legacyPrint won't actually modify it (risky if we lie)
    legacyPrint(const_cast<char*>(message));
    
    return 0;
}
```

### 8. `constexpr` (Modern C++)

`constexpr` is a much stronger form of const. It says that the value is known **at compile time**. This allows big optimizations. The compiler does the calculation, so the CPU does not have to do it at runtime.

```cpp
#include <iostream>

// This function can be evaluated at compile time
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : (n * factorial(n - 1));
}

int main() {
    constexpr int val = factorial(5);
    // The compiler simply replaces 'val' with 120 in the binary.
    
    std::cout << "Factorial(5): " << val << std::endl;
    return 0;
}
```

---

## New words

- **qualifier**: a word like `const` or `volatile` that changes how a variable behaves.
- **const**: cannot be changed.
- **mutable**: can be changed, even inside a `const` method.
- **volatile**: may change outside the program, so the compiler must read it every time.
- **register (hardware)**: a memory address that controls or reports on a piece of hardware.
- **compile time**: when the compiler builds your program. **Runtime** is when the program runs.
- **Undefined Behavior**: code that breaks the rules. The result can be anything.
