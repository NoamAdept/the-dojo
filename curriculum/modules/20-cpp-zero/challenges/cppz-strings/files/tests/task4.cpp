// Task 4: keyOf
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::string k = keyOf("gain=12");
    SAY(k == "gain", "keyOf(\"gain=12\") should be \"gain\" but was " << shown(k));
    k = keyOf("mode=fm=wide");
    SAY(k == "mode", "keyOf(\"mode=fm=wide\") should stop at the FIRST '=' and give \"mode\", but was " << shown(k));
    k = keyOf("antenna");
    SAY(k == "antenna", "keyOf(\"antenna\") has no '=', so it should return the whole line, but was " << shown(k));
}
