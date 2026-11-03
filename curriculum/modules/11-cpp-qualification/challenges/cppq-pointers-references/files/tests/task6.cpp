// Task 6: reverse in place
#include "check.h"
#include "tasks.h"
int main() {
    int odd[] = {1, 2, 3, 4, 5};
    reverseArray(odd, 5);
    EXPECT(odd[0] == 5 && odd[2] == 3 && odd[4] == 1);
    int even[] = {1, 2, 3, 4};
    reverseArray(even, 4);
    EXPECT(even[0] == 4 && even[1] == 3 && even[3] == 1);
    reverseArray(even, 0);
}
