// Task 4: file reader
#include <cstdio>
#include "check.h"
#include "tasks.h"
int main() {
    { std::ofstream("t4.txt") << "first line\nsecond\n"; }
    EXPECT(readFirstLine("t4.txt") == "first line");
    std::remove("t4.txt");
    EXPECT(readFirstLine("t4_missing.txt") == "");
}
