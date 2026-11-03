// Task 3: BankAccount invariant
#include "check.h"
#include "tasks.h"
int main() {
    BankAccount acct(100.0);
    acct.deposit(50.0);
    EXPECT(acct.withdraw(30.0) && acct.balance() == 120.0);
    EXPECT(!acct.withdraw(500.0) && acct.balance() == 120.0);
}
