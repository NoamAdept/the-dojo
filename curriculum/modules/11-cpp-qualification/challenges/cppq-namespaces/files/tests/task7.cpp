// Task 7: deep namespace hierarchy
#include "check.h"
#include "tasks.h"
int main() {
    namespace res = Company::Division::Department::Team::Resources;
    using Company::Division::Finance::Accounting::calculateBudget;
    EXPECT(res::Employee("Ada").getInfo() == "Employee: Ada");
    EXPECT(calculateBudget(1000.0, 3) == 3000.0);
}
