// Task 7: resource manager closes at scope end
#include "check.h"
#include "tasks.h"
int main() {
    {
        FileManager f("capture.iq");
        f.write("hello");
        EXPECT(g_events.back() == "hello");
    }
    EXPECT((g_events == std::vector<std::string>{"Opening capture.iq", "hello", "Closing capture.iq"}));
}
