// Task 2: perimeter
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Rectangle r{2.5, 4.0};
    SAY(r.perimeter() == 13.0, "a 2.5 by 4 rectangle should have perimeter() 13 but got " << r.perimeter());
}
