# Your First C++ Program

`cpf-first-program` · Orange Belt

**Goal:** Compile `hello.cpp` into a program called `hello`, then change it so it prints exactly two lines: `Hello, C++!` and `I can compile C++.`, and rebuild it.

**File `hello.cpp`**

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello, C++!\n";
    std::cout << "I can compile C++.\n";
    return 0;
}
```

Then type:

```bash
g++ -std=c++17 -Wall -Wextra hello.cpp -o hello
./hello
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
