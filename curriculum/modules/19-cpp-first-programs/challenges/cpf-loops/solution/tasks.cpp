#include <iostream>

// Task 1: return 1 + 2 + ... + n (use a while loop)
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

// Task 2: return 1 * 2 * ... * n (use a for loop)
int factorial(int n)
{
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Task 3: return how many digits n has (n is 0 or more)
int count_digits(int n)
{
    int digits = 1;
    while (n >= 10) {
        n /= 10;
        digits++;
    }
    return digits;
}

// Task 4: return base to the power exp (exp is 0 or more)
int power(int base, int exp)
{
    int result = 1;
    for (int i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

// Task 5: print n stars, then a new line
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
