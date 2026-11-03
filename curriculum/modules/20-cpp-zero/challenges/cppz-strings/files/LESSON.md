# Text with std::string: lesson

### One letter at a time: [ ]

`name[0]` gives one `char` of the string. The number in the square brackets is the **index**. The index is the position of the letter. Counting starts at **0**, not 1. So for `"Ada"`:

- `name[0]` is `'A'`
- `name[1]` is `'d'`
- `name[2]` is `'a'`

The last letter is at `name.size() - 1`. Do not ask for a position past the end. That is a bug. The program may print rubbish or crash. So always stay below `size()`.

### Joining needs a string on one side

Be careful: `"Hi, " + "there"` does not work. Neither side is a `std::string` yet. When one side is a `std::string` (like `name` above), `+` joins the text.

### Member functions

`greeting.size()` is a **member function**. A member function is a function that belongs to a value. To call it, write the variable, a dot, the function name and `()`. `size()` gives the number of characters.

The type of `size()` is `std::size_t`. This is a whole-number type for sizes and positions. It is never negative. Use it for loop counters that go along a string. Then the compiler does not warn you about mixing `int` and `std::size_t`:

```cpp
for (std::size_t i = 0; i < text.size(); i++) {
    if (text[i] == 'a') { /* ... */ }
}
```

### Finding and cutting

- `text.find('=')` gives the position of the first `=` (counting from 0). If there is no `=`, it gives a special value: `std::string::npos` ("no position").
- `text.substr(start, count)` gives a copy of `count` characters. The copy starts at `start`.
- `text.substr(start)` gives everything from `start` to the end.

```cpp
std::string line = "freq=433";
std::size_t pos = line.find('=');          // 4
std::string key = line.substr(0, pos);     // "freq"
std::string value = line.substr(pos + 1);  // "433"
if (line.find('#') == std::string::npos) {
    // there is no '#' in line
}
```

### Your code goes in a header file

In this module you write functions in a file called `tasks.h`. A **header** is a file of code that another file includes. To include it, the other file writes `#include "tasks.h"`. Use quotes for your own files. Use angle brackets for library files.

Each test in `tests/` includes your `tasks.h`. The test calls your functions and compares the answers. The `#pragma once` line at the top makes sure the file is included only once. Leave it there.

Do you want to try a function yourself? Make a file `play.cpp` next to `tasks.h`:

```cpp
#include <iostream>
#include "tasks.h"

int main() {
    std::cout << makeGreeting("Ada") << std::endl;
    return 0;
}
```

Then run `g++ -std=c++17 play.cpp -o play && ./play`.

Did you make a typo? Then `./check` says **does not compile yet**. It also shows the first error lines from the compiler, for example `tasks.h:9:5: error: ...`. This means: file `tasks.h`, line 9, column 5. Go to that line and read the message.

### New words

- **std::string**: a piece of text that grows and shrinks by itself.
- **index**: the position of one item, counted from 0. `name[0]` is the first letter.
- **member function**: a function that belongs to a value. You call it with a dot: `text.size()`.
- **size()**: the number of characters in a string.
- **std::size_t**: a whole-number type for sizes. It is never negative.
- **find**: gives the position of something in a string. It gives `std::string::npos` if the thing is not there.
- **std::string::npos**: the special "not found" position.
- **substr**: copies a piece of a string.
- **header (.h)**: a file of code that other files include with `#include`.
