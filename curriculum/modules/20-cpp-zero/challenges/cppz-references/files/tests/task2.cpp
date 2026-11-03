// Task 2: addOne (reference)
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int n = -1;
    addOne(n);
    SAY(n == 0, "after n = -1; addOne(n); n should be 0 but is " << n);
    addOne(n);
    addOne(n);
    SAY(n == 2, "after two more addOne(n) calls, n should be 2 but is " << n);
}
