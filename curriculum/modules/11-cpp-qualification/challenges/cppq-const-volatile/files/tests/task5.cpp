// Task 5: read-only Settings API
#include "check.h"
#include "tasks.h"
int main() {
    Settings s;
    s.setInt("gain", 30);
    const Settings& ro = s;
    EXPECT(ro.getInt("gain") == 30 && ro.getInt("missing") == -1);
}
