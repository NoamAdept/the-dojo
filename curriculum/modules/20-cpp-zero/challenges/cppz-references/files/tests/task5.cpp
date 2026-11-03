// Task 5: total with a const reference
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    const std::vector<int> v = {12, 30, -2};
    int t = total(v);
    SAY(t == 40, "total({12, 30, -2}) should be 40 but was " << t);
    SAY(v == std::vector<int>({12, 30, -2}), "total must not change the vector");
    const std::vector<int> e;
    SAY(total(e) == 0, "total of an empty vector should be 0");
}
