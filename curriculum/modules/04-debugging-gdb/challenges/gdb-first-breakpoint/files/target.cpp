#include <iostream>

static int checkpoint(int sample) { return sample / 3; }

int main() {
    int base = 17;
    int shifted = (base << 2) + 5;
    std::cout << checkpoint(shifted) << '\n';
    return 0;
}
