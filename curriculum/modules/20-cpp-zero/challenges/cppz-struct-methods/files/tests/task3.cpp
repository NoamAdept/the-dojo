// Task 3: scale
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Rectangle r{2.0, 5.0};
    r.scale(3.0);
    SAY(r.width == 6.0 && r.height == 15.0, "after r{2, 5}.scale(3), width should be 6 and height 15, but they are " << r.width << " and " << r.height);
    Rectangle other{1.0, 1.0};
    r.scale(0.5);
    SAY(other.width == 1.0, "scaling one rectangle must not change a different rectangle");
}
