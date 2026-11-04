# Decimals, Letters and Yes/No

`cpf-types` · Orange Belt

**Goal:** Add five lines to `types.cpp` that print `total=`, `grade=`, `next=`, `many=` and `average=` using `double`, `char`, `bool` and a cast to avoid integer division.

**File `types.cpp`**

```cpp
#include <iostream>
#include <iomanip>

int main()
{
    double price = 2.5;
    int count = 4;
    int sum = 7;
    int parts = 3;
    char grade = 'B';

    std::cout << "given: " << price << " " << count << " " << sum << " " << parts << " " << grade << "\n";

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "total=" << price * count << "\n";

    std::cout << "grade=" << grade << "\n";

    char next = grade + 1;
    std::cout << "next=" << next << "\n";

    bool many = count > 3;
    std::cout << "many=" << many << "\n";

    std::cout << "average=" << static_cast<double>(sum) / parts << "\n";

    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
