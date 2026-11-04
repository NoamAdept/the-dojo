# Functions: Inputs and Outputs

`cpf-functions` · Orange Belt

**Goal:** Fill in `add`, `square`, `to_fahrenheit` and `sum_of_squares` in `tasks.cpp`, write a brand new `perimeter` function, and print `perimeter(3, 4) = 14` from `main`.

**File `tasks.cpp`**

```cpp
#include <iostream>

int add(int a, int b)
{
    return a + b;
}

int square(int x)
{
    return x * x;
}

double to_fahrenheit(double celsius)
{
    return celsius * 9 / 5 + 32;
}

int perimeter(int width, int height)
{
    return 2 * width + 2 * height;
}

int sum_of_squares(int a, int b)
{
    return square(a) + square(b);
}

int main()
{
    std::cout << "add(2, 3) = " << add(2, 3) << "\n";
    std::cout << "square(4) = " << square(4) << "\n";
    std::cout << "to_fahrenheit(100.0) = " << to_fahrenheit(100.0) << "\n";
    std::cout << "sum_of_squares(3, 4) = " << sum_of_squares(3, 4) << "\n";
    std::cout << "perimeter(3, 4) = " << perimeter(3, 4) << "\n";
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
