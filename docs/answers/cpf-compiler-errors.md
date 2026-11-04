# Read a Compiler Error

`cpf-compiler-errors` · Orange Belt

**Goal:** Fix the one mistake in each of `oops1.cpp` to `oops4.cpp` so each file compiles and prints its line unchanged.

**File `oops1.cpp`**

```cpp
#include <iostream>

int main()
{
    std::cout << "Line one\n";
    std::cout << "Line two\n";
    return 0;
}
```

**File `oops2.cpp`**

```cpp
#include <iostream>

int main()
{
    std::cout << "Spelling matters\n";
    return 0;
}
```

**File `oops3.cpp`**

```cpp
#include <iostream>

int main()
{
    std::cout << "Braces come in pairs\n";
    return 0;
}
```

**File `oops4.cpp`**

```cpp
#include <iostream>

int main()
{
    std::cout << "Almost done\n";
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
