// Task 5: mostCommon
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::string w = mostCommon({"am", "usb", "usb", "fm", "usb", "am"});
    SAY(w == "usb", "mostCommon({am, usb, usb, fm, usb, am}) should be \"usb\" but was " << shown(w));
    w = mostCommon({"wfm", "nfm", "nfm", "wfm"});
    SAY(w == "nfm", "nfm and wfm both appear twice, so the alphabetically first, \"nfm\", should win, but got " << shown(w));
    w = mostCommon({"cw"});
    SAY(w == "cw", "mostCommon({\"cw\"}) should be \"cw\" but was " << shown(w));
}
