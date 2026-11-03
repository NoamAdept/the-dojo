// Task 3: sleepy thread
#include "check.h"
#include "tasks.h"
int main() {
    auto t0 = std::chrono::steady_clock::now();
    auto events = sleepyThread(200);
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now() - t0).count();
    EXPECT((events == std::vector<std::string>{"Start", "End"}));
    EXPECT(ms >= 200);
}
