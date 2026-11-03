// Task 3: version check
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(versionMatches("3.11.2", " 3.11.2\n"));
    EXPECT(!versionMatches("3.11.2", "3.11.3"));
}
