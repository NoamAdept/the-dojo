# Follow the Arrow

`cpp-pointer-basics` · Orange Belt

**Goal:** Fill in the four functions in `pointers.cpp` so they change values through pointers, sum a row of ints, and return a pointer (or `nullptr`) to a found item.

**File `pointers.cpp`**

```cpp
#include "pointers.hpp"

void add_one(int* x)
{
    *x = *x + 1;
}

void swap_ints(int* a, int* b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int sum_array(const int* values, std::size_t count)
{
    int total = 0;
    for (std::size_t i = 0; i < count; i++) {
        total += values[i];
    }
    return total;
}

int* find_value(int* values, std::size_t count, int wanted)
{
    for (std::size_t i = 0; i < count; i++) {
        if (values[i] == wanted) {
            return &values[i];
        }
    }
    return nullptr;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
