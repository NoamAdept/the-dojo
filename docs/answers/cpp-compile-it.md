# First Blood Compile

`cpp-compile-it` · Orange Belt

**Goal:** Make `meter.cpp` build with no messages under strict warning flags, compute a real average, and print it with exactly one digit after the point, so `./meter` prints `average=20.0`.

**File `meter.cpp`**

```cpp
#include <iomanip>
#include <iostream>

double average(double a, double b, double c) {
    int count = 3;
    return (a + b + c) / count;
}

void print_average(double value) {
    std::cout << "average=" << std::fixed << std::setprecision(1) << value << std::endl;
}

int main() {
    double first = 10.0;
    double second = 20.0;
    double third = 30.0;
    print_average(average(first, second, third));
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
