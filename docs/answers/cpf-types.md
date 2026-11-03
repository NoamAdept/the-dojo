## Decimals, Letters and Yes/No

*cpf-types · easy*

**Goal.** Add five lines to `types.cpp` that print `total=`, `grade=`, `next=`, `many=` and `average=` using `double`, `char`, `bool` and a cast to avoid integer division.

**You need to know.**

- `double` holds decimals; `std::fixed << std::setprecision(2)` shows two decimal places (needs `#include <iomanip>`, already there).
- A `char` is one character stored as a small number, so `grade + 1` is the next letter once it is stored in a `char`.
- A `bool` is true or false, and `std::cout` prints it as `1` or `0`.
- `static_cast<double>(x)` turns an int into a double before dividing.

**Walkthrough.**

1. Open `types.cpp`. Do not touch the five lines declaring `price`, `count`, `sum`, `parts` and `grade`; `./check` swaps in other values.

2. Task 1:

   ```cpp
   std::cout << std::fixed << std::setprecision(2);
   std::cout << "total=" << price * count << "\n";
   ```

   The first line changes how every later decimal is printed (always two places), so 2.5 x 4 shows as `10.00`.

3. Task 2:

   ```cpp
   std::cout << "grade=" << grade << "\n";
   ```

   Printing a `char` prints the letter itself.

4. Task 3:

   ```cpp
   char next = grade + 1;
   std::cout << "next=" << next << "\n";
   ```

   `grade + 1` is an int (67 for `'B'`); storing it in a `char` makes `std::cout` print it as the letter `C`.

5. Task 4:

   ```cpp
   bool many = count > 3;
   std::cout << "many=" << many << "\n";
   ```

   The comparison `count > 3` is itself true or false, and a bool prints as `1` or `0`.

6. Task 5:

   ```cpp
   std::cout << "average=" << static_cast<double>(sum) / parts << "\n";
   ```

   Turning `sum` into a double first makes the division a decimal division, so 7 / 3 gives `2.33` and not `2.00`.

7. Build, run and check.

   ```bash
   g++ -std=c++17 -Wall -Wextra types.cpp -o types
   ./types
   ./check
   ```

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- `std::cout << "next=" << grade + 1` prints `next=67`. Store the result in a `char` first.
- `static_cast<double>(sum / parts)` casts too late: the int division already threw the fraction away, so you still get `2.00`.
- Forgetting `std::fixed << std::setprecision(2)`, which prints `total=10` instead of `total=10.00`.
