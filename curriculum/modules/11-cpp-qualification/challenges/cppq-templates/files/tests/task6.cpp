// Task 6: MyPair<K, V>
#include "check.h"
#include "tasks.h"
int main() {
    MyPair<std::string, int> a("gain", 30);
    MyPair<int, double> b(7, 1.5);
    EXPECT(a.key == "gain" && a.value == 30);
    EXPECT(a.print() == "Key: gain, Value: 30" && b.print() == "Key: 7, Value: 1.5");
}
