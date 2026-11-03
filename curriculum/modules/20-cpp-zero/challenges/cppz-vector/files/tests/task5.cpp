// Task 5: longWords
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::vector<std::string> w = longWords({"sdr", "antenna", "iq", "radio", "fm"}, 3);
    SAY(w.size() == 3, "longWords({\"sdr\", \"antenna\", \"iq\", \"radio\", \"fm\"}, 3) should keep 3 words but kept " << w.size());
    SAY(w == std::vector<std::string>({"sdr", "antenna", "radio"}), "longWords should keep \"sdr\", \"antenna\", \"radio\" in that order");
    SAY(longWords({"a", "bb"}, 5).empty(), "longWords({\"a\", \"bb\"}, 5) should be empty");
}
