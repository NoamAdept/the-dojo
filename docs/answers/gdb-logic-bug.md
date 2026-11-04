# Wrong Answer, Right Place

`gdb-logic-bug` · Orange Belt

**Goal:** Step through the loop in GDB to see why every sample is counted, then fix the condition in `target.cpp` so samples from 10 to 20 inclusive count and the program prints `usable=4`.

**File `target.cpp`**

```cpp
#include <iostream>

int main() {
    int samples[] = {9, 10, 14, 20, 21, 17};
    int usable = 0;
    for (int i = 0; i < 6; i++) {
        if (samples[i] >= 10 && samples[i] <= 20) {
            usable++;
        }
    }
    std::cout << "usable=" << usable << '\n';
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
