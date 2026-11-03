// Task 1: makeGreeting
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    std::string g = makeGreeting("Grace");
    SAY(g == "Hello, Grace!", "makeGreeting(\"Grace\") should return \"Hello, Grace!\" but returned " << shown(g));
    g = makeGreeting("Linus");
    SAY(g == "Hello, Linus!", "makeGreeting(\"Linus\") should return \"Hello, Linus!\" but returned " << shown(g));
}
