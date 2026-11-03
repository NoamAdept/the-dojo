// Task 3: mutable cache in a const method
#include "check.h"
#include "tasks.h"
int main() {
    const Calculator c;
    EXPECT(c.heavyCalc() == 42 && c.heavyCalc() == 42);
    EXPECT(c.computations() == 1);
}
