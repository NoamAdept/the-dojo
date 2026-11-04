# Variables and Whole Numbers

`cpf-variables` · Orange Belt

**Goal:** Add four `std::cout` lines to `numbers.cpp` that print `apples=`, `total=`, `each=` and `left=` computed from the variables `apples` and `friends`.

**File `numbers.cpp`**

```cpp
#include <iostream>

int main()
{
    int apples = 7;
    int friends = 3;

    std::cout << "We have " << apples << " apples and " << friends << " friends.\n";

    std::cout << "apples=" << apples << "\n";

    std::cout << "total=" << apples + friends << "\n";

    std::cout << "each=" << apples / friends << "\n";

    std::cout << "left=" << apples % friends << "\n";

    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
