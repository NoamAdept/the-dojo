// Task 1: area
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Rectangle r{2.5, 4.0};
    SAY(r.area() == 10.0, "a 2.5 by 4 rectangle should have area() 10 but got " << r.area());
    Rectangle s{7.0, 1.0};
    SAY(s.area() == 7.0, "a 7 by 1 rectangle should have area() 7 but got " << s.area());
}
