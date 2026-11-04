# Capstone: A Signal Level Report

`cpf-capstone` · Orange Belt

**Goal:** Finish `report.cpp` so `./report -40 -72 -55` prints a five-line report (count, smallest, largest, average, strong count), and refuses bad input with a usage or "not a number" message.

**File `report.cpp`**

```cpp
#include <iostream>
#include <iomanip>
#include <string>

int larger(int a, int b)
{
    if (a > b) {
        return a;
    }
    return b;
}

int smaller(int a, int b)
{
    if (a < b) {
        return a;
    }
    return b;
}

bool is_strong(int level)
{
    return level >= -60;
}

double average(int total, int count)
{
    return static_cast<double>(total) / count;
}

int main(int argc, char* argv[])
{
    int count = argc - 1;
    if (count < 1) {
        std::cout << "usage: ./report LEVEL...\n";
        return 1;
    }

    int total = 0;
    int low = 0;
    int high = 0;
    int strong = 0;
    for (int i = 1; i < argc; i++) {
        int level = 0;
        try {
            level = std::stoi(argv[i]);
        } catch (...) {
            std::cout << "not a number: " << argv[i] << "\n";
            return 1;
        }
        if (i == 1) {
            low = level;
            high = level;
        }
        low = smaller(low, level);
        high = larger(high, level);
        total += level;
        if (is_strong(level)) {
            strong++;
        }
    }

    std::cout << "readings: " << count << "\n";
    std::cout << "smallest: " << low << "\n";
    std::cout << "largest: " << high << "\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "average: " << average(total, count) << "\n";
    std::cout << "strong: " << strong << "\n";
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
