// Task 5: semantic version ordering
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(SemVer("1.9.9") < SemVer("1.10.0"));
    EXPECT(SemVer("2.0.0") == SemVer("2.0.0") && !(SemVer("2.0.0") < SemVer("2.0.0")));
    EXPECT(SemVer("0.1.2") < SemVer("0.2.0") && !(SemVer("3.0.0") < SemVer("2.99.99")));
    bool threw = false;
    try { SemVer("1.x.3"); } catch (const std::invalid_argument&) { threw = true; }
    EXPECT(threw);
}
