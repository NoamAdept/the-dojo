// Task 4: null check
#include "check.h"
#include "tasks.h"
int main() {
    int x = 5;
    EXPECT(describe(&x) == "Value is: 5");
    EXPECT(describe(nullptr) == "Null Pointer");
}
