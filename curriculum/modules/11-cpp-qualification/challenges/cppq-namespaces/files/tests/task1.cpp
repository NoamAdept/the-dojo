// Task 1: Calculator namespace
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(Calculator::add(10, 5) == 15);
    EXPECT(Calculator::subtract(10, 5) == 5);
    EXPECT(Calculator::multiply(10, 5) == 50);
}
