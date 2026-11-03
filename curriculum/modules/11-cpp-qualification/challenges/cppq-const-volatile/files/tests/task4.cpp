// Task 4: constexpr array size
#include "check.h"
#include "tasks.h"
int arr[square(5)];
static_assert(kArraySize == 25, "square(5) must be usable at compile time");
int main() { EXPECT(sizeof(arr) / sizeof(arr[0]) == 25); }
