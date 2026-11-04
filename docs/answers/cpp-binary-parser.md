# Length-Prefixed Prey

`cpp-binary-parser` · Orange Belt

**Goal:** Write `parse_records` in `records.cpp` so it walks a buffer of type/length/payload records, calls a visitor for each complete one and refuses truncated input, then write `count_records` using your own visitor.

**File `records.cpp`**

```cpp
#include "records.hpp"

bool parse_records(const uint8_t* data, std::size_t size, record_visitor visit, void* context)
{
    std::size_t offset = 0;
    while (offset < size) {
        if (size - offset < 2) {
            return false;
        }
        uint8_t type = data[offset];
        std::size_t length = data[offset + 1];
        offset += 2;
        if (length > size - offset) {
            return false;
        }
        visit(type, data + offset, length, context);
        offset += length;
    }
    return true;
}

void count_one(uint8_t, const uint8_t*, std::size_t, void* context)
{
    int* n = static_cast<int*>(context);
    *n += 1;
}

int count_records(const uint8_t* data, std::size_t size)
{
    int n = 0;
    if (!parse_records(data, size, count_one, &n)) {
        return -1;
    }
    return n;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
