// Task 6: Result<T, E>
#include "check.h"
#include "tasks.h"
int main() {
    auto good = Result<int, std::string>::ok(7);
    auto bad = Result<int, std::string>::err("nope");
    EXPECT(good.isOk() && good.value() == 7);
    EXPECT(!bad.isOk() && bad.error() == "nope");
}
