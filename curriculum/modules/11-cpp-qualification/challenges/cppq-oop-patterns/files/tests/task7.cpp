// Task 7: Display and Alarm observers
#include "check.h"
#include "tasks.h"
int main() {
    Sensor sensor;
    Display display;
    Alarm alarm;
    sensor.attach(&display);
    sensor.attach(&alarm);
    for (int v : {50, 150, 99, 101}) sensor.notify(v);
    EXPECT(display.last() == 101);
    EXPECT(alarm.beeps() == 2);
}
