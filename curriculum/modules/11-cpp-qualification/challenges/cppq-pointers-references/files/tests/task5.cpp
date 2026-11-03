// Task 5: swap through pointers
#include "check.h"
#include "tasks.h"
int main() { int a = 1, b = 2; swap(&a, &b); EXPECT(a == 2 && b == 1); }
