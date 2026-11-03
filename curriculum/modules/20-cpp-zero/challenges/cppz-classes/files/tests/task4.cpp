// Task 4: Radio basics
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Radio r(101.1);
    SAY(r.frequency() == 101.1, "Radio r(101.1); r.frequency() should be 101.1 but was " << r.frequency());
    r.tune(94.5);
    SAY(r.frequency() == 94.5, "after r.tune(94.5), frequency() should be 94.5 but was " << r.frequency());
    Radio other(90.0);
    SAY(other.frequency() == 90.0 && r.frequency() == 94.5, "each Radio must keep its own frequency (use a field, not a global variable)");
}
