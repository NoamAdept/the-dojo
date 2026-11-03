// Task 1: catch std::out_of_range
#include "check.h"
#include "tasks.h"
int main() {
    std::vector<int> v{4, 2};
    EXPECT(safeAt(v, 1) == "2" && safeAt(v, 100) == "out_of_range");
}
