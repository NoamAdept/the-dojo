# Strings and Files: lesson

### 1. std::string Deep Dive

C-style strings (`char array[]`) are hard to use. `std::string` is a dynamic container for text. "Dynamic" means it can grow and shrink while the program runs.
- You include `<string>` to use it.
- You can join strings with `+`. This is called concatenation.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string greeting = "Hello";
    std::string name = "World";
    
    // Concatenation
    std::string message = greeting + ", " + name + "!";
    std::cout << message << std::endl;
    
    // Appending
    message += " How are you?";
    std::cout << message << std::endl;
    
    // Properties
    std::cout << "Length: " << message.length() << std::endl;
    std::cout << "Is empty? " << (message.empty() ? "Yes" : "No") << std::endl;
    
    return 0;
}

// Expected Output:
// Hello, World!
// Hello, World! How are you?
// Length: 26
// Is empty? No
```

### 2. Accessing Characters

A string is an array of characters. So you can read each `char` on its own.
- `[i]`: access without a check. It is fast.
- `at(i)`: access with a check. It throws an error if `i` is out of bounds (past the end).

```cpp
#include <iostream>
#include <string>

int main() {
    std::string text = "C++ is fun";
    
    char first = text[0];
    char last = text.at(text.length() - 1);
    
    std::cout << "First: " << first << ", Last: " << last << std::endl;
    
    // Strings are mutable (changeable)
    text[0] = 'c';
    std::cout << "Modified: " << text << std::endl;
    
    return 0;
}

// Expected Output:
// First: C, Last: n
// Modified: c++ is fun
```

### 3. Substrings & Find

- `find(sub)`: returns the index (position) where `sub` first appears. If it does not find `sub`, it returns `std::string::npos`.
- `substr(start, length)`: copies out one part of the string. This part is a substring.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string email = "user@example.com";
    
    // Find position of '@'
    size_t atPos = email.find('@');
    
    if (atPos != std::string::npos) {
        std::cout << "Found @ at index: " << atPos << std::endl;
        
        // Extract domain (everything after @)
        // substr(startIndex) goes to end if no length provided
        std::string domain = email.substr(atPos + 1);
        std::cout << "Domain: " << domain << std::endl;
    } else {
        std::cout << "Invalid email" << std::endl;
    }
    
    return 0;
}

// Expected Output:
// Found @ at index: 4
// Domain: example.com
```

### 4. String Conversion

Sometimes a number is stored as a string, like "123", and you need an `int`. Sometimes you need the opposite.
- `std::to_string(val)`: number -> string.
- `std::stoi(str)`: string -> int.
- `std::stod(str)`: string -> double.

```cpp
#include <iostream>
#include <string>

int main() {
    // Number to String
    int score = 42;
    std::string scoreMsg = "Score: " + std::to_string(score); // + works now
    std::cout << scoreMsg << std::endl;
    
    // String to Number
    std::string priceStr = "19.99";
    double price = std::stod(priceStr);
    std::cout << "Price + Tax: " << price * 1.1 << std::endl;
    
    return 0;
}

// Expected Output:
// Score: 42
// Price + Tax: 21.989
```

### 5. File I/O: Introduction

I/O means input and output. C++ does I/O with **streams**. A stream is a flow of data that you read from or write to.
- `iostream`: `cin`, `cout` (the console, or terminal)
- `fstream`: `ifstream` (read a file), `ofstream` (write a file)

Steps:
1. Open the file.
2. Check that it is open.
3. Read or write.
4. Close the file.

### 6. Writing to Files (`ofstream`)

To write, use an output file stream.

```cpp
#include <iostream>
#include <fstream> // Required for files

int main() {
    // Create output file stream and open "test.txt"
    std::ofstream outFile("test.txt");
    
    if (outFile.is_open()) {
        outFile << "Hello from C++ Files!\n";
        outFile << "This is a second line.\n";
        outFile << "Number: " << 12345 << "\n";
        
        outFile.close(); // Good practice to close
        std::cout << "File written successfully." << std::endl;
    } else {
        std::cout << "Unable to open file for writing." << std::endl;
    }
    
    return 0;
}

// Expected Output:
// File written successfully.
// (And a file 'test.txt' is created)
```

### 7. Reading from Files (`ifstream`)

There are 2 common ways to read:
- `file >> var`: reads one word at a time. It skips whitespace (spaces, tabs, newlines).
- `std::getline(file, line)`: reads a whole line.

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream inFile("test.txt");
    
    if (inFile.is_open()) {
        std::string line;
        std::cout << "--- Reading File Contents ---" << std::endl;
        
        // Loop until end of file
        while (std::getline(inFile, line)) {
            std::cout << line << std::endl;
        }
        
        inFile.close();
    } else {
        std::cout << "Unable to open file for reading." << std::endl;
    }
    
    return 0;
}

// Expected Output:
// --- Reading File Contents ---
// Hello from C++ Files!
// This is a second line.
// Number: 12345
```

### 8. File Modes

When you open a file, you can say how you want to use it. This is the file mode.
- `std::ios::out`: write. This is the default for ofstream.
- `std::ios::in`: read. This is the default for ifstream.
- `std::ios::app`: **append**. Add to the end. Do not erase what is already there.
- `std::ios::binary`: binary mode (raw bytes, not text).

```cpp
#include <iostream>
#include <fstream>

int main() {
    // Open in append mode
    std::ofstream outFile("test.txt", std::ios::app);
    
    if (outFile.is_open()) {
        outFile << "Appended line!\n";
        outFile.close();
    }
    
    return 0;
}
```

---

## New words

- **dynamic**: can change size while the program runs.
- **concatenation**: joining strings end to end.
- **index**: the position of an item. The first position is 0.
- **out of bounds**: an index that is past the end, or before the start.
- **stream**: a flow of data that you read from or write to.
- **append**: add to the end, and keep what is already there.
