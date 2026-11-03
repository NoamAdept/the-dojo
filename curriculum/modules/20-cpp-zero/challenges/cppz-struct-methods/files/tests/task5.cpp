// Task 5: makeSquare
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Rectangle r = makeSquare(4.5);
    SAY(r.width == 4.5 && r.height == 4.5, "makeSquare(4.5) should have width 4.5 and height 4.5, but has " << r.width << " and " << r.height);
}
