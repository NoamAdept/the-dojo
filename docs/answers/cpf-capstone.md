## Capstone: A Signal Level Report

*cpf-capstone · medium*

**Goal.** Finish `report.cpp` so `./report -40 -72 -55` prints a five-line report (count, smallest, largest, average, strong count), and refuses bad input with a usage or "not a number" message.

**You need to know.**

- Functions, `if`, and returning a comparison as a `bool` (earlier challenges in this module).
- `static_cast<double>` to avoid integer division, and `std::fixed << std::setprecision(2)`.
- `argc`/`argv`, `std::stoi` and `try`/`catch` (cpf-arguments).
- Running values in a loop: total, smallest, largest, counter.

**Walkthrough.**

1. Task 1, `smaller` (copy `larger` and flip the comparison):

   ```cpp
   if (a < b) {
       return a;
   }
   return b;
   ```

2. Task 2, `is_strong`:

   ```cpp
   return level >= -60;
   ```

   -60 itself counts as strong, so it must be `>=`.

3. Task 3, `average`:

   ```cpp
   return static_cast<double>(total) / count;
   ```

   Casting `total` first makes it a decimal division (-167 / 3 gives -55.67, not -55).

4. Task 5 first, at the top of `main`: the usage check.

   ```cpp
   int count = argc - 1;
   if (count < 1) {
       std::cout << "usage: ./report LEVEL...\n";
       return 1;
   }
   ```

   `argc` includes the program name, so the number of levels is `argc - 1`.

5. Tasks 4 and 5 together: one loop that converts, validates and keeps running values.

   ```cpp
   int total = 0;
   int low = 0;
   int high = 0;
   int strong = 0;
   for (int i = 1; i < argc; i++) {
       int level = 0;
       try {
           level = std::stoi(argv[i]);
       } catch (...) {
           std::cout << "not a number: " << argv[i] << "\n";
           return 1;
       }
       if (i == 1) {
           low = level;
           high = level;
       }
       low = smaller(low, level);
       high = larger(high, level);
       total += level;
       if (is_strong(level)) {
           strong++;
       }
   }
   ```

   The first reading seeds `low` and `high`, so starting them at 0 never wins against negative levels. A bad word returns before anything is printed.

6. After the loop, print the report:

   ```cpp
   std::cout << "readings: " << count << "\n";
   std::cout << "smallest: " << low << "\n";
   std::cout << "largest: " << high << "\n";
   std::cout << std::fixed << std::setprecision(2);
   std::cout << "average: " << average(total, count) << "\n";
   std::cout << "strong: " << strong << "\n";
   return 0;
   ```

7. Build and run:

   ```bash
   g++ -std=c++17 -Wall -Wextra report.cpp -o report
   ./report -40 -72 -55
   ./check
   ```

   Expected output: `readings: 3`, `smallest: -72`, `largest: -40`, `average: -55.67`, `strong: 2`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`. It runs the report on several sets, including random ones with up to 30 levels.

**Common mistakes.**

- Starting `high` (or `low`) at 0. With all-negative levels the largest then shows as 0. Seed both from the first reading.
- Printing report lines inside the loop, so `./report -40 loud` prints part of a report before the error. The check wants only `not a number: loud`.
- Using `> -60` instead of `>= -60`, so a level of exactly -60 is not counted as strong.
