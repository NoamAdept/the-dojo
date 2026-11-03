// Task 4: abstract Shape
#include <type_traits>
#include "check.h"
#include "tasks.h"
int main() {
    static_assert(std::is_abstract_v<Shape>, "Shape needs a pure virtual draw()");
    static_assert(std::has_virtual_destructor_v<Shape>, "Shape needs a virtual destructor");
    Circle c;
    Square s;
    const Shape& r = c;
    EXPECT(r.draw() == "circle" && s.draw() == "square");
}
