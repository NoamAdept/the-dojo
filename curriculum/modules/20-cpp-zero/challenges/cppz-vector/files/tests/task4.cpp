// Task 4: largest
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int m = largest({4, 17, 2, 9});
    SAY(m == 17, "largest({4, 17, 2, 9}) should be 17 but was " << m);
    m = largest({-8, -3, -12});
    SAY(m == -3, "largest({-8, -3, -12}) should be -3 but was " << m << " (did you start from 0 instead of v[0]?)");
    m = largest({42});
    SAY(m == 42, "largest({42}) should be 42 but was " << m);
}
