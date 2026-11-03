// Task 1: unique_ptr destroys automatically
#include "check.h"
#include "tasks.h"
int main() {
    { auto w = makeWidget(); EXPECT(w != nullptr); }
    EXPECT((g_events == std::vector<std::string>{"built", "broken"}));
}
