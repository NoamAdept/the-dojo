// Task 5: grade analyzer with sentinel
#include "check.h"
#include "tasks.h"
int main() {
    GradeReport r = analyzeGrades({80, 95, 70, -1, 100});
    EXPECT(r.count == 3 && r.max == 95 && r.average > 81.6 && r.average < 81.7);
}
