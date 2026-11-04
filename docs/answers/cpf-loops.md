# Repeating: while and for

`cpf-loops` · Orange Belt

**Goal:** Complete `sum_to`, `factorial`, `count_digits`, `power` and the void function `print_stars` in `tasks.cpp` using `while` and `for` loops.

**File `tasks.cpp`**

```cpp
#include <iostream>

int sum_to(int n)
{
    int total = 0;
    int i = 1;
    while (i <= n) {
        total += i;
        i++;
    }
    return total;
}

int factorial(int n)
{
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int count_digits(int n)
{
    int digits = 1;
    while (n >= 10) {
        n /= 10;
        digits++;
    }
    return digits;
}

int power(int base, int exp)
{
    int result = 1;
    for (int i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

void print_stars(int n)
{
    for (int i = 0; i < n; i++) {
        std::cout << '*';
    }
    std::cout << '\n';
}

int main()
{
    std::cout << "sum_to(4) = " << sum_to(4) << "\n";
    std::cout << "factorial(5) = " << factorial(5) << "\n";
    std::cout << "count_digits(2024) = " << count_digits(2024) << "\n";
    std::cout << "power(2, 10) = " << power(2, 10) << "\n";
    print_stars(3);
    return 0;
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
