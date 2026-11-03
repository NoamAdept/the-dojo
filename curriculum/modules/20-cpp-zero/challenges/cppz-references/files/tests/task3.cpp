// Task 3: swapValues
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int a = 7, b = 300;
    swapValues(a, b);
    SAY(a == 300 && b == 7, "after a = 7, b = 300; swapValues(a, b); a should be 300 and b should be 7, but a is " << a << " and b is " << b << ". Keep a's old value in a temporary variable first.");
}
