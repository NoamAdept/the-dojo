# Pointers and References: lesson

### What is Memory?

Think of computer memory (RAM) as a very long street of houses.
- Each house holds a value (data).
- Each house has its own **address** (for example, House #1024).

### 1. What is a Pointer? (`&` Operator)

A **Pointer** is a variable. It stores the **memory address** of another variable.

- You use the **Address-of Operator (`&`)** to get the address of a variable.
- Say you have `int a = 10;`. Then `&a` gives you the place in memory where `10` is stored.

```cpp
#include <iostream>

int main() {
    int number = 42;
    
    std::cout << "Value of number: " << number << std::endl;
    std::cout << "Address of number: " << &number << std::endl;
    
    return 0;
}

// Expected Output:
// Value of number: 42
// Address of number: 0x... (some hexadecimal address)
```

### 2. Declaring and Dereferencing (`*` Operator)

- **Declaration**: `Type* ptr;` (read it as "pointer to Type").
- **Dereferencing**: `*ptr` means "go to the address stored in `ptr` and use the value there".

Think of `ptr` as a piece of paper with a house address on it.
- `ptr` = the paper (it holds the address).
- `*ptr` = go to that house and look at what is inside.

```cpp
#include <iostream>

int main() {
    int value = 100;
    int* ptr = &value; // ptr now holds the address of 'value'
    
    std::cout << "Value via variable: " << value << std::endl;
    std::cout << "Value via pointer: " << *ptr << std::endl;
    
    // Changing value using pointer
    *ptr = 200;
    std::cout << "New value via variable: " << value << std::endl;
    
    return 0;
}

// Expected Output:
// Value via variable: 100
// Value via pointer: 100
// New value via variable: 200
```

### 3. The Null Pointer (`nullptr`)

Uninitialized pointers are dangerous! (Uninitialized means you never gave it a value.) Such a pointer holds a random address (garbage). If you use it, the program may do strange things or crash.

Always initialize pointers. If you do not have an address yet, use `nullptr`.

```cpp
#include <iostream>

int main() {
    int* ptr = nullptr; // Safe initialization
    
    if (ptr != nullptr) {
        std::cout << "Value: " << *ptr << std::endl;
    } else {
        std::cout << "Pointer is null, cannot dereference!" << std::endl;
    }
    
    int val = 10;
    ptr = &val;
    
    if (ptr) { // Shorthand for 'if (ptr != nullptr)'
        std::cout << "Pointer points to: " << *ptr << std::endl;
    }
    
    return 0;
}

// Expected Output:
// Pointer is null, cannot dereference!
// Pointer points to: 10
```

### 4. Pointers and Arrays

In C++, arrays and pointers are closely related. The name of an array works like a pointer to its first element.

**Pointer Arithmetic**: you can add a number to a pointer. This moves it to the next place in memory. The step size depends on the size of the type.

```cpp
#include <iostream>

int main() {
    int arr[] = {10, 20, 30};
    int* ptr = arr; // Points to arr[0]
    
    std::cout << "First element: " << *ptr << std::endl;
    
    ptr++; // Move to next integer
    std::cout << "Second element: " << *ptr << std::endl;
    
    std::cout << "Third element (using array syntax on pointer): " << ptr[1] << std::endl;
    
    return 0;
}

// Expected Output:
// First element: 10
// Second element: 20
// Third element (using array syntax on pointer): 30
```

### 5. What is a Reference?

A **Reference** is an **alias** (another name) for a variable that already exists.
- You declare it with `&` (for example, `int& ref = var;`).
- You must initialize it at once.
- It cannot be null.
- After it is bound to (joined to) a variable, it cannot refer to a different one.

```cpp
#include <iostream>

int main() {
    int original = 500;
    int& ref = original;
    
    std::cout << "Original: " << original << std::endl;
    std::cout << "Reference: " << ref << std::endl;
    
    ref = 600; // Changing ref changes original
    
    std::cout << "Original after modification: " << original << std::endl;
    
    return 0;
}

// Expected Output:
// Original: 500
// Reference: 500
// Original after modification: 600
```

### 6. Pointers vs References

| Feature | Pointer (`*`) | Reference (`&`) |
|---------|--------------|-----------------|
| Memory Address | Stores address | Is an alias |
| Nullability | Can be `nullptr` | Cannot be null |
| Resettable | Can point to new things | Cannot bind to new variable |
| Syntax | Needs dereferencing (`*`) | Use like normal variable |

**Guideline:** Use **References** when you can. They are safer and the code is cleaner. Use **Pointers** when you must, for example for:
- dynamic memory (memory you ask for while the program runs)
- optional values (a value that may be missing)
- pointer arithmetic

```cpp
#include <iostream>

void passByPointer(int* p) {
    if (p) {
        *p = *p + 10;
    }
}

void passByReference(int& r) {
    r = r + 10;
}

int main() {
    int a = 10, b = 10;
    
    passByPointer(&a);
    passByReference(b);
    
    std::cout << "A: " << a << ", B: " << b << std::endl;
    return 0;
}

// Expected Output:
// A: 20, B: 20
```

### 7. Pointers to Pointers

A pointer can point to another pointer.
- Declaration: `int** ptr2ptr;`
- Dereference 2 times, `**ptr2ptr`, to get the value.

```cpp
#include <iostream>

int main() {
    int var = 123;
    int* ptr = &var;
    int** ptr2ptr = &ptr;
    
    std::cout << "Value: " << var << std::endl;
    std::cout << "Value via ptr: " << *ptr << std::endl;
    std::cout << "Value via ptr2ptr: " << **ptr2ptr << std::endl;
    
    return 0;
}

// Expected Output:
// Value: 123
// Value via ptr: 123
// Value via ptr2ptr: 123
```

### 8. Const Correctness

Pointers work with `const` in 2 ways. Read the type from right to left:
1. `const int* p` -> a pointer to a **constant integer**. You cannot change the value.
2. `int* const p` -> a **constant pointer** to an integer. You cannot change the address.

### 9. Casting in C++

Changing a value from one type to another is called **Casting**. In C, you wrote `(type)value`. C++ has special cast operators. They are safer, and they show clearly what you want.

#### 9.1 C-Style Cast (Avoid this!)
- `(int)3.5` or `int(3.5)`.
- **Problem**: it tries to do *anything*. It may convert, reinterpret bits, or remove const. It does not check if this is safe. It is also hard to find with grep (a text search tool).

#### 9.2 `static_cast` (Use this for values)
- It converts between related types. Examples: int to float, enum to int, pointer to a parent class.
- The compiler checks it at compile time.
```cpp
double pi = 3.14;
int x = static_cast<int>(pi); // Explicit conversion
```

#### 9.3 `reinterpret_cast` (Use this for bits)
- It treats the raw bits of a pointer or reference as another type.
- It is very dangerous. But low-level code needs it, for example hardware drivers.
```cpp
int* p = &x;
char* bytes = reinterpret_cast<char*>(p); // Treat int as array of chars
```

#### 9.4 `const_cast` (Use this for const)
- It adds or removes `const`.
- Use it only when you *know* the original object was not really const. Or use it for old (legacy) APIs.

```cpp
#include <iostream>

int main() {
    int x = 10;
    int y = 20;
    
    // Case 1: Pointer to const int
    const int* p1 = &x;
    // *p1 = 30; // Error: Cannot change value
    p1 = &y;     // OK: Can change address
    
    // Case 2: Const Pointer to int
    int* const p2 = &x;
    *p2 = 30;    // OK: Can change value
    // p2 = &y;  // Error: Cannot change address
    
    std::cout << "X is now: " << x << std::endl;
    return 0;
}

// Expected Output:
// X is now: 30
```

---

## New words

- **address**: the place in memory where a value is stored.
- **pointer**: a variable that holds an address.
- **dereference**: go to the address and use the value there.
- **nullptr**: a pointer value that means "points to nothing".
- **reference**: another name (alias) for an existing variable.
- **pointer arithmetic**: adding to or subtracting from a pointer to move through memory.
- **cast**: changing a value from one type to another.
