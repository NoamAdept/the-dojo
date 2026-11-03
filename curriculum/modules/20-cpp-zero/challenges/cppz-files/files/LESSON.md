# Reading and Writing Text Files: lesson

### Reading line by line

```cpp
#include <fstream>
#include <string>

std::ifstream in("notes.txt");   // open the file for reading
if (!in) {
    // the file could not be opened (missing, no permission, ...)
}
std::string line;
while (std::getline(in, line)) {
    // line holds one line of the file, without the "\n" at the end
}
```

- `std::ifstream` is an **input file stream**: a file opened for reading.
- `if (!in)` is true when the file could not be opened. Always check it.
- `std::getline(in, line)` reads the next line into `line`. When there are no more lines, it returns something that counts as `false`. This ends the `while` loop.
- You never close the file yourself. It closes automatically when `in` goes away, at the end of the function. C++ does this a lot. An object cleans up after itself when it is no longer needed.

### Text to number

You already used `std::stoi` ("string to int") with `argv` in C++ First Programs:

- `std::stoi("42")` is `42`.
- `std::stoi("-7")` is `-7`.

A line that you read from a file is also a `std::string`. So `std::stoi(line)` works. Do not give it an empty line. An empty line stops the program with an error. So check `line.empty()` first. It is `true` when the string has no characters.

### Writing a file

`std::ofstream` is an **output file stream**: a file opened for writing. You write to it with `<<`, in the same way as `std::cout`:

```cpp
std::ofstream out("report.txt");   // creates the file (or empties it)
if (!out) {
    // could not create it, for example the folder does not exist
}
out << "gain=" << 30 << "\n";
```

### Try it in the terminal

```
vim sample.txt
```

Follow these steps in vim:

1. Press `i`.
2. Type `one`, `two` and `three` on 3 lines.
3. Press `Esc`.
4. Save and quit with `:wq`.

Now you have a file with 3 lines. Use it to test your functions with a small `play.cpp`. For example: `std::cout << countLines("sample.txt") << std::endl;`.

### New words

- **stream**: something you read from or write to, in order. For example `std::cout` or a file.
- **std::ifstream**: a file opened for reading.
- **std::ofstream**: a file opened for writing.
- **std::getline(in, line)**: reads one line (without its `\n`) into `line`.
- **std::stoi**: turns text like `"42"` into the int 42.
- **closes automatically**: the file closes by itself when the stream variable goes away.
