// Task 7: POSIX signal as an interrupt
#include "check.h"
#include "tasks.h"
int main() {
    installSignalIsr(SIGUSR1);
    EXPECT(g_signalSeen == 0);
    std::raise(SIGUSR1);
    EXPECT(g_signalSeen == 1);
}
