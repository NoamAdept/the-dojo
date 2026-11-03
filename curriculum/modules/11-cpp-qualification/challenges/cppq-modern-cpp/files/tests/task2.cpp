// Task 2: inline function vs macro
#include "check.h"
#include "tasks.h"
int main() {
    int a = 5;
    EXPECT(square(a++) == 25 && a == 6);
    EXPECT(macroSurprise() == 2);
}
