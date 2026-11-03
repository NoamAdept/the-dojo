// Task 2: atomic counter
#include "check.h"
#include "tasks.h"
int main() { EXPECT(atomicCount(100000) == 200000); }
