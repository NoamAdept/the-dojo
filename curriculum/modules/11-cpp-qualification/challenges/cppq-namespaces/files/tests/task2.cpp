// Task 2: scope resolution
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(::counter == 0 && Game::counter == 10 && Game::Player::counter == 100);
    Game::counter = 11;
    EXPECT(sumCounters() == 111);
}
