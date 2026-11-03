# Templates and Generic Programming: lesson

### 1. Function Templates

A function template is a pattern. The compiler uses it to make (generate) real functions.

Syntax:

```cpp
template <typename T>
void myFunction(T arg) { ... }
```

`T` is a placeholder for a type (like int, double, string). You write the code once. The compiler fills in the real type later.

```cpp
#include <iostream>
#include <string>

// Define a template function
template <typename T>
void printValue(T value) {
    std::cout << "Value: " << value << std::endl;
}

int main() {
    printValue(42);         // T is int
    printValue(3.14);       // T is double
    printValue("Hello");    // T is const char*
    printValue(std::string("World")); // T is std::string
    
    return 0;
}

// Expected Output:
// Value: 42
// Value: 3.14
// Value: Hello
// Value: World
```

### 2. Instantiation

Instantiation means the compiler makes a real function from the template.

When you call `printValue(42)`, the compiler makes a version of the function where `T` is `int`. This is called **Implicit Instantiation**. "Implicit" means the compiler finds the type by itself.

You can also give the type yourself (explicitly):

```cpp
printValue<int>(42.5); // Forces T to be int, 42.5 becomes 42
```

### 3. Multiple Template Parameters

A template can have more than 1 type placeholder.

```cpp
#include <iostream>

template <typename T, typename U>
void printPair(T first, U second) {
    std::cout << first << " -> " << second << std::endl;
}

int main() {
    printPair(1, "Apple");      // int, const char*
    printPair("Age", 30);       // const char*, int
    printPair(10.5, 20.5);      // double, double
    
    return 0;
}

// Expected Output:
// 1 -> Apple
// Age -> 30
// 10.5 -> 20.5
```

### 4. Class Templates

Classes can be generic too, just like functions. `std::vector` is a class template!

Let's make a generic "Box" that can hold any item.

```cpp
#include <iostream>

template <typename T>
class Box {
private:
    T item;
    
public:
    Box(T i) : item(i) {}
    
    T getItem() {
        return item;
    }
    
    void setItem(T i) {
        item = i;
    }
};

int main() {
    Box<int> intBox(123);
    std::cout << "Int Box: " << intBox.getItem() << std::endl;
    
    Box<std::string> strBox("Gift");
    std::cout << "String Box: " << strBox.getItem() << std::endl;
    
    return 0;
}

// Expected Output:
// Int Box: 123
// String Box: Gift
```

### 5. Non-Type Template Parameters

Templates can also take values, not only types. Usually these are integers. The value must be known at compile time (when the compiler builds the program).

`std::array<int, 5>` uses this. It is a container of 5 ints.

```cpp
#include <iostream>

template <typename T, int Size>
class FixedArray {
private:
    T data[Size]; // Size is known at compile time!
public:
    void set(int index, T value) {
        if (index >= 0 && index < Size) {
            data[index] = value;
        }
    }
    
    T get(int index) {
        if (index >= 0 && index < Size) return data[index];
        return T(); // Return default
    }
};

int main() {
    FixedArray<int, 3> arr;
    arr.set(0, 10);
    arr.set(1, 20);
    arr.set(2, 30);
    
    std::cout << arr.get(1) << std::endl;
    
    return 0;
}

// Expected Output:
// 20
```

### 6. Template Specialization

Sometimes the generic code does not work for one type. For example, `char` behaves differently from `int`. Then you can write a special version of the template for that type. This is called specialization.

```cpp
#include <iostream>

// Primary template
template <typename T>
void printType(T val) {
    std::cout << "Generic type print: " << val << std::endl;
}

// Specialization for char
template <>
void printType(char val) {
    std::cout << "Special CHAR print: '" << val << "'" << std::endl;
}

int main() {
    printType(100);
    printType('A');
    return 0;
}

// Expected Output:
// Generic type print: 100
// Special CHAR print: 'A'
```

---

## New words

- **generic programming**: writing code once so that it works with many types.
- **template**: a pattern that the compiler uses to make functions or classes for each type.
- **type parameter** (`T`): a placeholder name for a type.
- **instantiation**: the compiler makes real code from a template for one type.
- **specialization**: a special version of a template for one type.
