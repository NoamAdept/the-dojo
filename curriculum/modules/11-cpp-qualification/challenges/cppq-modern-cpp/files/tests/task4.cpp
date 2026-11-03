// Task 4: average with auto
#include <cmath>
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(std::fabs(average({1.1, 2.2, 3.3, 4.4, 5.5}) - 3.3) < 1e-9);
    EXPECT(average({}) == 0.0);
}
