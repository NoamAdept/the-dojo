// Task 6: PrimeChecker smart cache
#include "check.h"
#include "tasks.h"
int main() {
    const PrimeChecker p;
    EXPECT(p.isPrime(97) && p.isPrime(97) && !p.isPrime(1) && !p.isPrime(91) && p.isPrime(2));
    EXPECT(p.calculations() == 4);
}
