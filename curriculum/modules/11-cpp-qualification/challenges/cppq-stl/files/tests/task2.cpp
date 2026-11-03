// Task 2: map phonebook
#include "check.h"
#include "tasks.h"
int main() {
    std::map<std::string, std::string> book{{"ann", "555-1"}, {"bo", "555-2"}, {"cy", "555-3"}};
    EXPECT(lookup(book, "bo") == "555-2" && lookup(book, "zed") == "not found");
    EXPECT(book.size() == 3);
}
