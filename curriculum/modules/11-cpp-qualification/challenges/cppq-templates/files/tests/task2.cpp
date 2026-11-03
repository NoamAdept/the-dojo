// Task 2: generic adder
#include "check.h"
#include "tasks.h"
int main() { EXPECT(add(2, 3) == 5 && add(std::string("Pi "), std::string("SDR")) == "Pi SDR"); }
