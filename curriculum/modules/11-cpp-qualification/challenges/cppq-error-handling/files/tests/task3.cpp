// Task 3: optional parser
#include "check.h"
#include "tasks.h"
int main() { EXPECT(parsePositive(5) == 5 && !parsePositive(0) && !parsePositive(-3)); }
