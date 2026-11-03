#include <iostream>

static void inspect_here(int level) {
    volatile int visible = level;  // keeps this function from being empty
    (void)visible;
}

int main() {
    int samples[] = {3, 7, -2, 9, 4};
    int level = 10;
    for (int sample : samples) {
        level += sample;
        inspect_here(level);
    }
    std::cout << level << '\n';
    return 0;
}
