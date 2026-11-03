// Task 4: doubleAll
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::vector<int> v = {1, -4, 10};
    doubleAll(v);
    SAY(v == std::vector<int>({2, -8, 20}), "after doubleAll on {1, -4, 10}, v should be {2, -8, 20} but v[0] is " << v[0] << ". Did you loop with int& so the real items change?");
    std::vector<int> e;
    doubleAll(e);
    SAY(e.empty(), "doubleAll on an empty vector should leave it empty");
}
