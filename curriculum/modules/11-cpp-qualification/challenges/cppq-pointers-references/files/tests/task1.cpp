// Task 1: address-of
#include "check.h"
#include "tasks.h"
int main() { int num = 99; EXPECT(addressOf(num) == &num && *addressOf(num) == 99); }
