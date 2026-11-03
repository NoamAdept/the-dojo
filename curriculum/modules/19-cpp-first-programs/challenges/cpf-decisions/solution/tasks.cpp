#include <iostream>

// Task 1: return the larger of a and b
int bigger(int a, int b)
{
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

// Task 2: return true if n is even, false if odd
bool is_even(int n)
{
    return n % 2 == 0;
}

// Task 3: return 1, -1 or 0
int sign(int n)
{
    if (n > 0) {
        return 1;
    } else if (n < 0) {
        return -1;
    } else {
        return 0;
    }
}

// Task 4: return true if low <= x <= high
bool in_range(int x, int low, int high)
{
    return x >= low && x <= high;
}

// Task 5: return 'A', 'B', 'C' or 'F'
char grade_letter(int score)
{
    if (score >= 90) {
        return 'A';
    } else if (score >= 80) {
        return 'B';
    } else if (score >= 70) {
        return 'C';
    } else {
        return 'F';
    }
}

int main()
{
    std::cout << "bigger(3, 8) = " << bigger(3, 8) << "\n";
    std::cout << "is_even(6) = " << is_even(6) << "\n";
    std::cout << "sign(-5) = " << sign(-5) << "\n";
    std::cout << "in_range(5, 1, 10) = " << in_range(5, 1, 10) << "\n";
    std::cout << "grade_letter(85) = " << grade_letter(85) << "\n";
    return 0;
}
