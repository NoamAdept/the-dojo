// Task 6: Sensor notifies observers
#include "check.h"
#include "tasks.h"
struct Spy : Observer {
    int calls = 0, value = 0;
    void update(int v) override { ++calls; value = v; }
};
int main() {
    Sensor sensor;
    Spy a, b;
    sensor.attach(&a);
    sensor.attach(&b);
    sensor.notify(42);
    EXPECT(a.calls == 1 && b.calls == 1 && a.value == 42);
}
