# The Crash Site

`gdb-segfault` · Orange Belt

**Goal:** Use the AddressSanitizer report and GDB to find the out-of-range read in `largest`, then fix `target.cpp` so it builds cleanly and prints `largest=12`.

**File `target.cpp`**

```cpp
#include <iostream>
#include <vector>

static int largest(const std::vector<int> &values) {
    if (values.empty()) return 0;  // no samples: nothing to compare
    int best = values[0];
    for (std::size_t i = 1; i < values.size(); ++i) {
        if (values[i] > best) best = values[i];
    }
    return best;
}

int main() {
    std::vector<int> values = {4, 12, 7, -1};
    std::cout << "largest=" << largest(values) << '\n';
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
