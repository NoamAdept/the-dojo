// Task 1: const pointer to mutable int
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    static_assert(std::is_same_v<ConstPtrToInt, int* const>, "ConstPtrToInt must be int* const");
    int x = 10;
    ConstPtrToInt p = makeConstPtr(x);
    *p = 20;
    EXPECT(x == 20);
}
