#include <iomanip>
#include <iostream>

// Returns the average of three readings.
double average(double a, double b, double c) {
    int count = 3;
    return (a + b + c) / count;
}

// Prints "average=" and the value with exactly one digit after the point.
void print_average(double value) {
    std::cout << "average=" << std::fixed << std::setprecision(1) << value << std::endl;
}

int main() {
    double first = 10.0;
    double second = 20.0;
    double third = 30.0;
    print_average(average(first, second, third));
    return 0;
}
