// Task 5: valueOf
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::string v = valueOf("gain=12");
    SAY(v == "12", "valueOf(\"gain=12\") should be \"12\" but was " << shown(v));
    v = valueOf("mode=fm=wide");
    SAY(v == "fm=wide", "valueOf(\"mode=fm=wide\") should be everything after the FIRST '=', \"fm=wide\", but was " << shown(v));
    v = valueOf("antenna");
    SAY(v == "", "valueOf(\"antenna\") has no '=', so it should return \"\" but was " << shown(v));
    v = valueOf("empty=");
    SAY(v == "", "valueOf(\"empty=\") should be \"\" but was " << shown(v));
}
