// Task 6: CSV parser
#include "check.h"
#include "tasks.h"
int main() {
    Product p = parseProduct("Apple,1.50,100");
    EXPECT(p.name == "Apple" && p.price == 1.5 && p.quantity == 100);
    EXPECT(totalValue(p) == 150.0);
    EXPECT(parseProduct("Raspberry Pi 5 kit,1299.99,3").name == "Raspberry Pi 5 kit");
}
