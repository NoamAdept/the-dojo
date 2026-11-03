// Task 1: plusOne (pass by value)
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int n = 41;
    int r = plusOne(n);
    SAY(r == 42, "plusOne(41) should return 42 but returned " << r);
    SAY(n == 41, "after plusOne(n), n should still be 41 because x is only a copy, but n is " << n);
    r = plusOne(-8);
    SAY(r == -7, "plusOne(-8) should return -7 but returned " << r);
}
