// Task 5: Radio rules
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    Radio r(100.0);
    r.tune(150.0);
    SAY(r.frequency() == 100.0, "tune(150.0) is outside 88..108 and should be ignored, but frequency() became " << r.frequency());
    r.tune(87.9);
    SAY(r.frequency() == 100.0, "tune(87.9) is outside 88..108 and should be ignored, but frequency() became " << r.frequency());
    r.tune(108.0);
    SAY(r.frequency() == 108.0, "tune(108.0) is allowed (108 itself is in range), but frequency() is " << r.frequency());
    r.tune(88.0);
    SAY(r.frequency() == 88.0, "tune(88.0) is allowed (88 itself is in range), but frequency() is " << r.frequency());
    Radio bad(5.0);
    SAY(bad.frequency() == 88.0, "Radio bad(5.0) starts outside the range, so the constructor should use 88.0, but frequency() is " << bad.frequency());
}
