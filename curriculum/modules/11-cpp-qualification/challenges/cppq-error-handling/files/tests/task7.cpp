// Task 7: file loader returns error enums
#include "check.h"
#include "tasks.h"
int main() {
    auto ok = loadFile("data/iq.cfg");
    EXPECT(ok.isOk() && ok.value() == "contents of data/iq.cfg");
    EXPECT(loadFile("secret.cfg").error() == LoadError::Denied);
    EXPECT(loadFile("tmp/x").error() == LoadError::NotFound);
}
