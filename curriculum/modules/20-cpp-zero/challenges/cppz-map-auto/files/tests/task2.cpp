// Task 2: lookup
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    const std::map<std::string, int> m = {{"gain", 30}, {"ppm", 0}, {"rate", 2400}};
    int v = lookup(m, "rate");
    SAY(v == 2400, "lookup(m, \"rate\") should be 2400 but was " << v);
    v = lookup(m, "ppm");
    SAY(v == 0, "lookup(m, \"ppm\") should be 0 (the key exists, its value is 0) but was " << v);
    v = lookup(m, "squelch");
    SAY(v == -1, "lookup(m, \"squelch\") should be -1 because that key is missing, but was " << v);
    SAY(m.size() == 3, "lookup must not add keys to the map");
}
