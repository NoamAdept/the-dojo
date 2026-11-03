// Task 3: simple logger
#include <cstdio>
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(writeLog("t3_log.txt", "Log Entry 1: System Started"));
    std::ifstream in("t3_log.txt");
    std::string line;
    std::getline(in, line);
    std::remove("t3_log.txt");
    EXPECT(line == "Log Entry 1: System Started");
    EXPECT(!writeLog("/no/such/dir/log.txt", "x"));
}
