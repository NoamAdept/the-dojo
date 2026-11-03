// Task 4: safe division
#include "check.h"
#include "tasks.h"
int main() { EXPECT(safeDivide(1.f, 4.f).value() == 0.25f && !safeDivide(1.f, 0.f)); }
