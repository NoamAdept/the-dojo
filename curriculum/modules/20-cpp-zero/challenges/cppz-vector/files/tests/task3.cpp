// Task 3: makeRange
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::vector<int> r = makeRange(5);
    SAY(r.size() == 5, "makeRange(5) should have 5 numbers but has " << r.size());
    SAY(r == std::vector<int>({1, 2, 3, 4, 5}), "makeRange(5) should be {1, 2, 3, 4, 5} in that order");
    SAY(makeRange(1) == std::vector<int>({1}), "makeRange(1) should be {1}");
    SAY(makeRange(0).empty(), "makeRange(0) should be an empty vector");
    SAY(makeRange(-3).empty(), "makeRange(-3) should be an empty vector");
}
