// Task 3: nested namespaces
#include "check.h"
#include "tasks.h"
int main() {
    namespace payroll = Organization::HR::Payroll;
    EXPECT(payroll::calculateSalary(5000.0, 1000.0) == 6000.0);
}
