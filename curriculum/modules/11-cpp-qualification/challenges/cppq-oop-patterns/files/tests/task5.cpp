// Task 5: shape factory
#include "check.h"
#include "tasks.h"
int main() {
    auto c = makeShape("circle");
    auto s = makeShape("square");
    EXPECT(c && c->draw() == "circle");
    EXPECT(s && s->draw() == "square");
    EXPECT(makeShape("hexagon") == nullptr);
}
