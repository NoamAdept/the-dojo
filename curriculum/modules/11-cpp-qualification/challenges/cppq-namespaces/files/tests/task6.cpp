// Task 6: Banking account and transfer
#include "check.h"
#include "tasks.h"
int main() {
    Banking::Account a(1, 100.0), b(2, 0.0);
    a.deposit(50);
    EXPECT(a.balance() == 150.0);
    EXPECT(!a.withdraw(1000) && a.balance() == 150.0);
    EXPECT(Banking::transferFunds(a, b, 120.0));
    EXPECT(a.balance() == 30.0 && b.balance() == 120.0);
    EXPECT(!Banking::transferFunds(a, b, 31.0) && a.balance() == 30.0);
}
