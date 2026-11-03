// Task 7: custom comparator sort
#include "check.h"
#include "tasks.h"
int main() {
    std::vector<Player> p{{"cy", 50}, {"ann", 90}, {"bo", 50}, {"dee", 70}};
    rankPlayers(p);
    EXPECT(p[0].name == "ann" && p[1].name == "dee" && p[2].name == "bo" && p[3].name == "cy");
}
