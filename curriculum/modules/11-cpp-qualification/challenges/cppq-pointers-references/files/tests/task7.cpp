// Task 7: single-pass min and max
#include "check.h"
#include "tasks.h"
int main() {
    int data[] = {7, -3, 12, 0, 12, -8, 4};
    int lo = 0, hi = 0;
    findMinMax(data, 7, &lo, &hi);
    EXPECT(lo == -8 && hi == 12);
    int one[] = {42};
    findMinMax(one, 1, &lo, &hi);
    EXPECT(lo == 42 && hi == 42);
}
