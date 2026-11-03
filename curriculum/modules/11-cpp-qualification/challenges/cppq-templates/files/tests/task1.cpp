// Task 1: generic swap
#include "check.h"
#include "tasks.h"
int main() {
    int a = 1, b = 2;
    mySwap(a, b);
    std::string s = "x", t = "y";
    mySwap(s, t);
    EXPECT(a == 2 && b == 1 && s == "y" && t == "x");
}
