## Classes: Private Data and Constructors

*cppz-classes · easy*

**Goal.** Finish the `Counter` class (constructor, `value`, `increment`, private `count`) and write the `Radio` class with a private frequency field that only accepts 88.0 to 108.0 MHz.

**You need to know.**

- A class is a struct whose members can be `public:` (anyone may use) or `private:` (only the class's own methods) (README lesson).
- A constructor has the class name and no return type; it runs when the object is created, like `Counter c(7);`.
- Each object has its own copy of the fields.
- Checking rules in one method (here `tune`) and reusing it keeps the object always valid.

**Walkthrough.**

1. Task 1, in `Counter`:

   ```cpp
   Counter(int start) {
       count = start;
   }

   int value() { return count; }
   ```

   The constructor sets the starting value, and `value()` is the public way to read it.

2. Task 2, `increment`:

   ```cpp
   void increment() { count = count + 1; }
   ```

3. Task 3: put a `private:` label on the line above the field, at the bottom of `Counter`.

   ```cpp
   private:
       int count = 0;
   };
   ```

   Everything after `private:` is hidden from code outside the class; the test checks that `c.count` no longer compiles from outside.

4. Task 4, `Radio` basics. Add the private field at the bottom of the class:

   ```cpp
   private:
       double mhz;
   ```

   and use it in the methods (first version, no rules yet):

   <!-- draft: replaced in step 5 -->
   ```cpp
   Radio(double startMhz) { mhz = startMhz; }
   double frequency() { return mhz; }
   void tune(double newMhz) { mhz = newMhz; }
   ```

   Using a field (not a global variable) gives each radio its own frequency.

5. Task 5, the rules. Final versions of `tune` and the constructor:

   ```cpp
   void tune(double newMhz) {
       if (newMhz >= 88.0 && newMhz <= 108.0) {
           mhz = newMhz;
       }
   }

   Radio(double startMhz) {
       mhz = 88.0;
       tune(startMhz);
   }
   ```

   `tune` only stores values in range and silently ignores others. The constructor starts at the safe 88.0 and then lets `tune` decide, so the rule is written only once.

6. Run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Forgetting `private:` (task 3 fails with "code outside Counter can still use c.count"), or putting `private:` above the methods, which then cannot be called from the tests.
- Using `>` and `<` in `tune`, so the edge values 88.0 and 108.0 are wrongly ignored.
- In the constructor calling `tune(startMhz)` without first setting `mhz = 88.0`. A bad start value then leaves `mhz` uninitialised (garbage).
