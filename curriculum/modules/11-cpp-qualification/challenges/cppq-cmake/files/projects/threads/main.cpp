#include <iostream>
#include <thread>
int main() {
    int result = 0;
    std::thread t([&] { result = 7; });
    t.join();
    std::cout << "thread result " << result << "\n";
}
