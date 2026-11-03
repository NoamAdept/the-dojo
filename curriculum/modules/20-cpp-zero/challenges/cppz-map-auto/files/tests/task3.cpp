// Task 3: totalOfValues
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    const std::map<std::string, int> m = {{"a", 5}, {"b", -2}, {"c", 40}};
    int t = totalOfValues(m);
    SAY(t == 43, "totalOfValues of {a:5, b:-2, c:40} should be 43 but was " << t);
    SAY(totalOfValues({}) == 0, "totalOfValues of an empty map should be 0");
}
