# Input from the Command Line

`cpf-arguments` · Orange Belt

**Goal:** Finish two programs: `greet.cpp` (`./greet NAME` prints `Hello, NAME!`, with a usage message when no name is given) and `add.cpp` (adds any number of whole numbers and rejects words that are not numbers).

**File `add.cpp`**

```cpp
#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    int total = 0;
    for (int i = 1; i < argc; i++) {
        try {
            total += std::stoi(argv[i]);
        } catch (...) {
            std::cout << "not a number: " << argv[i] << "\n";
            return 1;
        }
    }
    std::cout << total << "\n";
    return 0;
}
```

**File `greet.cpp`**

```cpp
#include <iostream>

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cout << "usage: ./greet NAME\n";
        return 1;
    }
    std::cout << "Hello, " << argv[1] << "!\n";
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
