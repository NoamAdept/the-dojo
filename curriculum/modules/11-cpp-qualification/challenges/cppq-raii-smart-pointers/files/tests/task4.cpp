// Task 4: RAII scope logger
#include "check.h"
#include "tasks.h"
int main() {
    { ScopeLogger log("testFunction"); g_events.push_back("work"); }
    EXPECT((g_events == std::vector<std::string>{"Enter: testFunction", "work", "Exit: testFunction"}));
}
