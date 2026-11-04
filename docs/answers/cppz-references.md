# References: Another Name for a Variable

`cppz-references` · Orange Belt

**Goal:** Fill in `plusOne`, `addOne`, `swapValues`, `doubleAll` and `total` in `tasks.h`, seeing the difference between a copy, a reference (`int&`) and a `const` reference.

**File `tasks.h`**

```cpp
#pragma once
#include <vector>

int plusOne(int x) {
    return x + 1;
}

void addOne(int& x) {
    x = x + 1;
}

void swapValues(int& a, int& b) {
    int old = a;
    a = b;
    b = old;
}

void doubleAll(std::vector<int>& v) {
    for (int& x : v) x = x * 2;
}

int total(const std::vector<int>& v) {
    int sum = 0;
    for (int x : v) sum += x;
    return sum;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
