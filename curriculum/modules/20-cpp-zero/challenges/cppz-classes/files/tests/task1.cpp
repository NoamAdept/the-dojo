// Task 1: Counter constructor and value()
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Counter c(7);
    SAY(c.value() == 7, "Counter c(7); c.value() should be 7 but was " << c.value());
    Counter d(-2);
    SAY(d.value() == -2, "Counter d(-2); d.value() should be -2 but was " << d.value());
}
