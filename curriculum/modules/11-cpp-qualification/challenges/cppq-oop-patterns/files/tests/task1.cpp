// Task 1: Dog class basics
#include "check.h"
#include "tasks.h"
int main() {
    Dog d;
    d.setAge(5);
    d.setAge(31);
    d.setAge(-1);
    EXPECT(d.age() == 5 && d.bark() == "Woof!");
}
