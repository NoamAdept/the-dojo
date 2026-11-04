# Structs That Do Things

`cppz-struct-methods` · Orange Belt

**Goal:** Give the `Rectangle` struct in `tasks.h` four member functions (`area`, `perimeter`, `scale`, `isSquare`) and finish the free function `makeSquare`.

**File `tasks.h`**

```cpp
#pragma once

struct Rectangle {
    double width;
    double height;

    double area() { return width * height; }

    double perimeter() { return 2 * (width + height); }

    void scale(double factor) {
        width = width * factor;
        height = height * factor;
    }

    bool isSquare() { return width == height; }
};

Rectangle makeSquare(double side) {
    Rectangle r{side, side};
    return r;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
