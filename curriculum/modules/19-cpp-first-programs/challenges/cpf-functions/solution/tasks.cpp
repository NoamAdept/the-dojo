#include <iostream>

// Task 1: return a plus b
int add(int a, int b)
{
    return a + b;
}

// Task 2: return x times x
int square(int x)
{
    return x * x;
}

// Task 3: return celsius * 9 / 5 + 32
double to_fahrenheit(double celsius)
{
    return celsius * 9 / 5 + 32;
}

// Task 4: write int perimeter(int width, int height) here, all by yourself
int perimeter(int width, int height)
{
    return 2 * width + 2 * height;
}

// Task 5: return a*a + b*b, using your square function
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
