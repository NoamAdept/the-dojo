// Task 6: callback dispatcher
#include "check.h"
#include "tasks.h"
static int fired = 0;
static void onIrq() { ++fired; }
int main() {
    Global_ISR();  // nothing registered yet: must not crash
    InterruptManager::registerCallback(onIrq);
    Global_ISR();
    InterruptManager::registerCallback([] { fired += 10; });  // captureless lambda -> function pointer
    Global_ISR();
    EXPECT(fired == 11);
}
