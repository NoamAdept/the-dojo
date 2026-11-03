// Task 4: describe
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    const std::map<std::string, int> m = {{"zeta", 9}, {"alpha", 12}, {"mid", 0}};
    std::string d = describe(m);
    SAY(d == "alpha=12;mid=0;zeta=9;", "describe should give \"alpha=12;mid=0;zeta=9;\" (sorted order) but gave " << shown(d));
    d = describe({});
    SAY(d == "", "describe of an empty map should be \"\" but was " << shown(d));
}
