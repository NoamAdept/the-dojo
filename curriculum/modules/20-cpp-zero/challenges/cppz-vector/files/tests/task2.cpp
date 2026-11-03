// Task 2: countAbove
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int n = countAbove({1, 8, 3, 9, 5}, 4);
    SAY(n == 3, "countAbove({1, 8, 3, 9, 5}, 4) should be 3 but was " << n);
    n = countAbove({4, 4, 4}, 4);
    SAY(n == 0, "countAbove({4, 4, 4}, 4) should be 0 (4 is not bigger than 4) but was " << n);
}
