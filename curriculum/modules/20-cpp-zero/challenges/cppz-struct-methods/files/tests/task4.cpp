// Task 4: isSquare
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Rectangle sq{3.0, 3.0};
    Rectangle wide{3.0, 2.0};
    SAY(sq.isSquare(), "a 3 by 3 rectangle should be a square");
    SAY(!wide.isSquare(), "a 3 by 2 rectangle should not be a square");
}
