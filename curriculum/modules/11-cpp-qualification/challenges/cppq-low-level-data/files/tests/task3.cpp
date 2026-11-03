// Task 3: packed Header
#include <cstddef>
#include "check.h"
#include "tasks.h"
static_assert(sizeof(Header) == 4, "Header must be 4 bytes");
int main() { EXPECT(offsetof(Header, flags) == 2 && offsetof(Header, len) == 3); }
