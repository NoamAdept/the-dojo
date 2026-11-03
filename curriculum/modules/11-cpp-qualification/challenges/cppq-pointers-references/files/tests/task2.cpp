// Task 2: modify through a pointer
#include "check.h"
#include "tasks.h"
int main() { int score = 50; doubleViaPointer(&score); EXPECT(score == 100); }
