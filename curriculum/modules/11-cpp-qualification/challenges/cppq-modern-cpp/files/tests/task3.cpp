// Task 3: std::optional
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(getName(1).value_or("") == "Alice");
    EXPECT(!getName(2).has_value());
}
