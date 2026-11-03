// Task 7: volatile hardware register
#include "check.h"
#include "tasks.h"
int main() {
    volatile int* reg = new int(0);
    std::thread device(hardwareWrite, reg, 0xFFFF, 100);
    int got = waitForSignal(reg, 0xFFFF);
    device.join();
    delete reg;
    EXPECT(got == 0xFFFF);
}
