// Task 5: smart factory
#include "check.h"
#include "tasks.h"
int main() { auto p = createObject(7); EXPECT(p && *p == 7); }
