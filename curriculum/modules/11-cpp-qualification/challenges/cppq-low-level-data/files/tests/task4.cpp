// Task 4: power of two
#include "check.h"
#include "tasks.h"
int main() {
    for (int p : {1, 2, 4, 1024, 1 << 30}) EXPECT(isPowerOfTwo(p));
    for (int n : {0, -4, 3, 6, 1023}) EXPECT(!isPowerOfTwo(n));
}
