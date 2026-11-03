# Namespaces and Scope Resolution: lesson

### What are Namespaces?

A namespace is a C++ feature that groups code under a name. It keeps your code organized. It also stops two things with the same name from clashing (a naming conflict).

Think of a namespace as a box. The box holds identifiers. An identifier is the name of a variable, a function, a class, and so on. Names in one box stay separate from names in other boxes.

#### Why do we need namespaces?

Imagine a large project that uses many libraries. Two libraries might both have a function with the same name, for example `print()` or `calculate()`. Without namespaces, these names clash. The compiler then gives errors. A namespace fixes this. It puts related code under one unique name.

### 1. Creating a Basic Namespace

This is how you create a namespace:

```cpp
namespace namespace_name {
    // declarations and definitions
}
```

Here is a real example:

```cpp
#include <iostream>

namespace MathOps {
    int add(int a, int b) {
        return a + b;
    }
    
    int multiply(int a, int b) {
        return a * b;
    }
}

namespace StringOps {
    void add(std::string a, std::string b) {
        std::cout << "Concatenation: " << a + b << std::endl;
    }
}

int main() {
    // Using functions from MathOps namespace
    std::cout << "5 + 3 = " << MathOps::add(5, 3) << std::endl;
    std::cout << "5 * 3 = " << MathOps::multiply(5, 3) << std::endl;
    
    // Using function from StringOps namespace
    StringOps::add("Hello, ", "World!");
    
    return 0;
}

// Expected output:
// 5 + 3 = 8
// 5 * 3 = 15
// Concatenation: Hello, World!
```

**Notice:** `MathOps` and `StringOps` both have an `add` function. They do not clash, because they are in different namespaces.

### 2. The Scope Resolution Operator (::)

The **scope resolution operator** is `::`. You use it to reach a member of a namespace. It tells the compiler exactly which namespace holds the name you want.

#### Syntax:
```cpp
namespace_name::identifier
```

#### Examples:

```cpp
#include <iostream>

namespace Company {
    std::string name = "TechCorp";
    int employees = 100;
    
    void displayInfo() {
        std::cout << "Company: " << name << std::endl;
        std::cout << "Employees: " << employees << std::endl;
    }
}

int main() {
    // Accessing namespace members using ::
    std::cout << "Accessing via scope resolution:" << std::endl;
    std::cout << Company::name << std::endl;
    std::cout << Company::employees << std::endl;
    Company::displayInfo();
    
    return 0;
}

// Expected output:
// Accessing via scope resolution:
// TechCorp
// 100
// Company: TechCorp
// Employees: 100
```

### 3. Using Declarations and Directives

C++ has 2 ways to bring namespace members into the current scope. (A scope is the part of the code where a name is visible.)

#### 3.1 Using Declaration (`using namespace_name::identifier`)
This brings **one specific member** into the current scope.

```cpp
#include <iostream>

namespace Graphics {
    void drawCircle() { std::cout << "Drawing a circle" << std::endl; }
    void drawSquare() { std::cout << "Drawing a square" << std::endl; }
    void drawTriangle() { std::cout << "Drawing a triangle" << std::endl; }
}

int main() {
    // Using declaration for a specific function
    using Graphics::drawCircle;
    
    drawCircle();  // No need for Graphics:: prefix
    Graphics::drawSquare();  // Still need prefix for other members
    
    return 0;
}

// Expected output:
// Drawing a circle
// Drawing a square
```

#### 3.2 Using Directive (`using namespace namespace_name`)
This brings **all members** of a namespace into the current scope.

⚠️ **Warning:** Be careful with using directives. Be extra careful in header files. They can cause naming conflicts.

```cpp
#include <iostream>

namespace Audio {
    void play() { std::cout << "Playing audio" << std::endl; }
    void pause() { std::cout << "Pausing audio" << std::endl; }
    void stop() { std::cout << "Stopping audio" << std::endl; }
}

int main() {
    // Using directive for entire namespace
    using namespace Audio;
    
    // All Audio functions are now directly accessible
    play();
    pause();
    stop();
    
    return 0;
}

// Expected output:
// Playing audio
// Pausing audio
// Stopping audio
```

### 4. Nested Namespaces

You can put a namespace inside another namespace. This is a nested namespace. It helps you build a hierarchy (levels, like folders inside folders) for your code.

#### Traditional Syntax:
```cpp
namespace outer {
    namespace inner {
        // declarations
    }
}
```

#### C++17 Simplified Syntax:
```cpp
namespace outer::inner {
    // declarations
}
```

```cpp
#include <iostream>

namespace Company {
    namespace Department {
        namespace Engineering {
            void work() {
                std::cout << "Engineering team is working" << std::endl;
            }
        }
    }
}

// C++17 style (equivalent to above)
namespace Sales::Team {
    void sell() {
        std::cout << "Sales team is selling" << std::endl;
    }
}

int main() {
    // Accessing nested namespace members
    Company::Department::Engineering::work();
    Sales::Team::sell();
    
    // Using declaration with nested namespaces
    using namespace Company::Department::Engineering;
    work();  // Now we can call it directly
    
    return 0;
}

// Expected output:
// Engineering team is working
// Sales team is selling
// Engineering team is working
```

### 5. Anonymous (Unnamed) Namespaces

An **anonymous namespace** is a namespace with no name. Its members have **internal linkage**. This means only the same translation unit can see them. A translation unit is one source file after the preprocessor has run.

The `static` keyword on global variables and functions does a similar job. The anonymous namespace is the modern C++ way.

```cpp
#include <iostream>

namespace {
    // These are only visible in this file
    int secretValue = 42;
    
    void helperFunction() {
        std::cout << "This is a private helper function" << std::endl;
    }
}

int main() {
    // We can use anonymous namespace members directly
    std::cout << "Secret value: " << secretValue << std::endl;
    helperFunction();
    
    return 0;
}

// Expected output:
// Secret value: 42
// This is a private helper function
```

### 6. Global Namespace and the :: Operator

The **global namespace** is the default namespace. Code lives there when you do not name a namespace. You can write `::` with no namespace name before it. This means "use the name from the global namespace".

```cpp
#include <iostream>

int value = 100;  // Global namespace

namespace MySpace {
    int value = 200;  // MySpace namespace
    
    void display() {
        int value = 300;  // Local variable
        
        std::cout << "Local value: " << value << std::endl;
        std::cout << "MySpace::value: " << MySpace::value << std::endl;
        std::cout << "Global value: " << ::value << std::endl;  // :: accesses global
    }
}

int main() {
    MySpace::display();
    return 0;
}

// Expected output:
// Local value: 300
// MySpace::value: 200
// Global value: 100
```

### 7. Namespace Aliases

Namespace names can get very long, especially nested ones. A **namespace alias** is a shorter name for a namespace. It makes code easier to read and type.

```cpp
#include <iostream>

namespace VeryLongCompanyName {
    namespace Department {
        namespace SubDepartment {
            void process() {
                std::cout << "Processing in SubDepartment" << std::endl;
            }
        }
    }
}

int main() {
    // Without alias - verbose
    VeryLongCompanyName::Department::SubDepartment::process();
    
    // With alias - much cleaner!
    namespace vln = VeryLongCompanyName::Department::SubDepartment;
    vln::process();
    
    return 0;
}

// Expected output:
// Processing in SubDepartment
// Processing in SubDepartment
```

### 8. Header Files and the Preprocessor

Large C++ projects split code into 2 kinds of files:

- **Header Files (.h / .hpp)**: declarations (what exists).
- **Source Files (.cpp)**: the code that does the work.

#### 8.1 The `#include` Directive
The preprocessor runs *before compilation*. It copies the content of the included file into the current file.
- `#include <iostream>`: a standard library header. The compiler searches the system paths.
- `#include "my_header.h"`: your own header. The compiler searches the local folder first.

#### 8.2 Include Guards
Sometimes a header gets included more than once. For example, A includes B, and C also includes B. Then the same things are defined twice, and you get redefinition errors. **Include Guards** stop this.

**Traditional Way:**
```cpp
##ifndef MY_HEADER_H
##define MY_HEADER_H

// Declarations go here

##endif
```

**Modern Way (most compilers support it):**
```cpp
##pragma once

// Declarations go here
```

#### 8.3 Forward Declarations
Sometimes you do not need the full definition of a class. You only need to say that it exists, for example to use a pointer to it. A **Forward Declaration** such as `class MyClass;` does this. It compiles faster than including the whole header.

### 9. Best Practices

Follow these rules when you work with namespaces:

1. **Avoid `using namespace` in header files.** It adds all those names for every file that includes the header. This "pollutes" their namespace.
2. **Use `using` declarations only a little.** Use them only for names you use often, and only in a small scope.
3. **Prefer the full namespace name.** `std::cout` is clearer than just `cout`.
4. **Use namespace aliases for long names.** They make code easier to read.
5. **Use anonymous namespaces for helpers that only one file needs.** Use them instead of `static` functions.
6. **Put related code in the same namespace.** Logical groups make code easier to maintain.
7. **Do not nest namespaces too deeply.** 2 or 3 levels is usually the maximum.

---

## New words

- **namespace**: a named box that holds names, so they do not clash with other names.
- **identifier**: the name of a variable, function, class, and so on.
- **scope**: the part of the code where a name is visible.
- **scope resolution operator (`::`)**: the operator that picks which scope a name comes from.
- **internal linkage**: only the same source file can see the name.
- **translation unit**: one source file after the preprocessor has run.
- **alias**: a second, shorter name for the same thing.
- **include guard**: code that stops a header from being included twice.
