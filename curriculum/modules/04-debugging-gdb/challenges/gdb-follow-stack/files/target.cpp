#include <iostream>

[[gnu::noinline]] static int capture(int x) { return x + 1; }
[[gnu::noinline]] static int demodulate(int x) { return capture(x * 2); }
[[gnu::noinline]] static int receive(int x) { return demodulate(x + 3); }

int main() {
    std::cout << receive(4) << '\n';
    return 0;
}
