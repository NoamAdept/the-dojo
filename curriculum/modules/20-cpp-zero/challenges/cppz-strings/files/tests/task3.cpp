// Task 3: isYes
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    SAY(isYes("yes"), "isYes(\"yes\") should be true");
    SAY(isYes("y"), "isYes(\"y\") should be true");
    SAY(!isYes("no"), "isYes(\"no\") should be false");
    SAY(!isYes("yes please"), "isYes(\"yes please\") should be false: only exactly \"yes\" or \"y\" count");
    SAY(!isYes(""), "isYes(\"\") should be false");
}
