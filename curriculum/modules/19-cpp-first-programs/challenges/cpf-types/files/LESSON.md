# Decimals, Letters and Yes/No: lesson

### double: numbers with a decimal point

An `int` cannot hold 2.5. For numbers like this, C++ has the type `double`. The name is short for "double precision". It means "quite exact".

```cpp
double price = 2.5;
std::cout << price << "\n";        // prints 2.5
```

Sometimes you want to always show exactly 2 decimals. To do this, send 2 settings to `std::cout`. Do it once, before you print. These settings need the line `#include <iomanip>` at the top of the file. "iomanip" means "io manipulators": tools that change how input and output look.

```cpp
std::cout << std::fixed << std::setprecision(2);
std::cout << price << "\n";        // prints 2.50
std::cout << 2.333 << "\n";        // prints 2.33 (it rounds)
```

- `std::fixed` means "write decimals in the normal way".
- `std::setprecision(2)` means "with 2 digits after the decimal point".
- The settings stay on. They are used for every number that you print after them.

Sometimes you mix an `int` and a `double` in a calculation. Then C++ first changes the int into a double. So the result is a double:

```cpp
int count = 4;
double total = price * count;      // 10.0
```

### The integer-division trap

Look at the two sides of `/`. If **both** sides are ints, C++ divides with whole numbers. This is true even when you store the result in a double:

```cpp
int sum = 7;
int parts = 3;
double wrong = sum / parts;                         // 2.0 : the .33 is lost before storing
double right = static_cast<double>(sum) / parts;    // 2.333...
```

`static_cast<double>(sum)` is a **cast**. A cast changes a value into another type. Here it changes `sum` into a double. Then the division keeps its decimals.

### char: a single character

A **character** is one letter, digit or symbol. Its type is `char`. You write a char between single quote marks:

```cpp
char grade = 'B';
std::cout << grade << "\n";        // prints B
```

Single quotes, like `'B'`, mean one character. Double quotes, like `"B"`, mean text. These are different things.

Inside the computer, a char is only a small number. `'A'` is 65, `'B'` is 66, `'C'` is 67, and so on. This list of numbers is called **ASCII**. Because of this, you can do arithmetic with letters.

But the result of `grade + 1` is an `int`. std::cout prints an int as a number. To see a letter, first store the result in a `char`:

```cpp
std::cout << grade + 1 << "\n";    // prints 67
char next = grade + 1;
std::cout << next << "\n";         // prints C
```

### bool: yes or no

A `bool` holds one of 2 values: `true` or `false`. It is very good for the answer to a question. For example: "is count bigger than 3?". `>` means "greater than". `<` means "less than".

```cpp
bool many = count > 3;             // true when count is 4
std::cout << many << "\n";         // prints 1
```

std::cout prints `true` as `1` and `false` as `0`. (You will use bools a lot in the challenge about decisions.)

### New words

- double: the type for numbers with a decimal point, like 2.5.
- std::fixed, std::setprecision(2): settings for std::cout. Together they print exactly 2 decimals. They need `#include <iomanip>`.
- cast: `static_cast<double>(x)`. It changes x into a double.
- char: the type for one character. You write it in single quotes, like `'B'`.
- ASCII: the standard list of numbers for characters. 'A' is 65.
- bool: the type for yes/no. It holds `true` or `false`. It prints as 1 or 0.

## Offline help

- Offline: `man ascii` shows the full table of character numbers.
