#include <iostream>

int main() {
    int samples[] = {9, 10, 14, 20, 21, 17};
    int usable = 0;
    for (int i = 0; i < 6; i++) {
        if (samples[i] > 10 || samples[i] < 20) {
            usable++;
        }
    }
    std::cout << "usable=" << usable << '\n';
    return 0;
}
