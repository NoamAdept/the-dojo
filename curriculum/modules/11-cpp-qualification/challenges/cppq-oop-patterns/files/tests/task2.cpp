// Task 2: Logger singleton
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    static_assert(!std::is_copy_constructible_v<Logger>, "delete the copy constructor");
    Logger& a = Logger::instance();
    Logger& b = Logger::instance();
    EXPECT(&a == &b);
    int before = a.count();
    b.log("tuner locked");
    EXPECT(a.count() == before + 1);
}
