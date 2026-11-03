// Task 5: Geometry
#include <cmath>
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(std::fabs(Geometry::circleArea(1.0) - M_PI) < 1e-9);
    EXPECT(Geometry::rectangleArea(2.0, 3.5) == 7.0);
}
