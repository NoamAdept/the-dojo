// Task 1: data race vs mutex
#include "check.h"
#include "tasks.h"
int main() {
    int racy = racyCount(100000);
    EXPECT(racy > 0 && racy <= 200000);
    EXPECT(lockedCount(100000) == 200000);
}
