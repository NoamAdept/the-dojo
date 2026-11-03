// Task 3: count is private
#include <type_traits>
#include <utility>
#include "check.h"
#include "explain.h"
#include "tasks.h"
// Detects whether code outside the class can read .count.
template <class T, class = void> struct CountIsPublic : std::false_type {};
template <class T> struct CountIsPublic<T, std::void_t<decltype(std::declval<T&>().count)>> : std::true_type {};
int main() {
    SAY(!CountIsPublic<Counter>::value, "code outside Counter can still use c.count. Put a private: label on the line above the count field.");
    Counter c(1);
    c.increment();
    SAY(c.value() == 2, "after making count private, Counter c(1) plus one increment should give 2, but gave " << c.value());
}
