// Task 2: const reference accepts a temporary
#include "check.h"
#include "tasks.h"
int main() { EXPECT(printData(MyData{5}) == 5); }
