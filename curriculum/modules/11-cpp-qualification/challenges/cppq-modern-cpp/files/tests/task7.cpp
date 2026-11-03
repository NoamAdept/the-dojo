// Task 7: compile-time powers
#include "check.h"
#include "tasks.h"
static_assert(power(2, 4) == 16 && power(3, 0) == 1, "power must be constexpr");
int main() {
    auto a = makePowersOfTwo();
    static_assert(a.size() == 16);
    EXPECT(a[0] == 1 && a[10] == 1024 && a[15] == 32768);
}
