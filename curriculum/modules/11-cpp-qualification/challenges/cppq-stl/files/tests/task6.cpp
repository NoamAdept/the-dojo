// Task 6: word frequency
#include "check.h"
#include "tasks.h"
int main() {
    auto f = wordFrequency("dog cat dog apple cat dog");
    EXPECT(f["dog"] == 3 && f["cat"] == 2 && f["apple"] == 1 && f.size() == 3);
}
