// Task 1: sumAll
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int s = sumAll({5, 10, -2, 7});
    SAY(s == 20, "sumAll({5, 10, -2, 7}) should be 20 but was " << s);
    s = sumAll({});
    SAY(s == 0, "sumAll of an empty vector should be 0 but was " << s);
}
