// Task 5: ring buffer
#include "check.h"
#include "tasks.h"
int main() {
    RingBuffer rb{};
    for (char c : {'A', 'B', 'C'}) EXPECT(rb.push(c));
    uint8_t out = 0;
    EXPECT(rb.pop(out) && out == 'A' && rb.pop(out) && out == 'B' && rb.pop(out) && out == 'C');
    EXPECT(!rb.pop(out));
    int pushed = 0;
    while (rb.push(uint8_t(pushed))) ++pushed;
    EXPECT(pushed == 15);
    for (int i = 0; i < 15; ++i) EXPECT(rb.pop(out) && out == i);
}
