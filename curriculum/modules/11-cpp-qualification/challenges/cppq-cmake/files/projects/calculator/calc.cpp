#include <iostream>
#include <string>
std::string ui();
std::string history();
consteval int answer() { return 42; }  // consteval needs C++20
int main() { std::cout << ui() << "+" << history() << (answer() == 42 ? " ok" : " bad") << "\n"; }
