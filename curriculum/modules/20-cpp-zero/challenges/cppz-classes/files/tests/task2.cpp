// Task 2: Counter increment()
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Counter c(10);
    c.increment();
    c.increment();
    c.increment();
    SAY(c.value() == 13, "Counter c(10) after 3 increments should have value() 13 but has " << c.value());
}
