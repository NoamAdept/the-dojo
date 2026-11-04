# Text with std::string

`cppz-strings` · Orange Belt

**Goal:** Fill in the five functions in `tasks.h` (`makeGreeting`, `countChar`, `isYes`, `keyOf`, `valueOf`) using `std::string` joining, comparing, indexing, `find` and `substr`.

**File `tasks.h`**

```cpp
#pragma once
#include <string>

std::string makeGreeting(std::string name) {
    return "Hello, " + name + "!";
}

int countChar(std::string text, char c) {
    int count = 0;
    for (std::size_t i = 0; i < text.size(); i++) {
        if (text[i] == c) count++;
    }
    return count;
}

bool isYes(std::string answer) {
    return answer == "yes" || answer == "y";
}

std::string keyOf(std::string line) {
    std::size_t pos = line.find('=');
    if (pos == std::string::npos) return line;
    return line.substr(0, pos);
}

std::string valueOf(std::string line) {
    std::size_t pos = line.find('=');
    if (pos == std::string::npos) return "";
    return line.substr(pos + 1);
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
