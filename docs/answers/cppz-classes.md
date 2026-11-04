# Classes: Private Data and Constructors

`cppz-classes` · Orange Belt

**Goal:** Finish the `Counter` class (constructor, `value`, `increment`, private `count`) and write the `Radio` class with a private frequency field that only accepts 88.0 to 108.0 MHz.

**File `tasks.h`**

```cpp
#pragma once

class Counter {
public:
    Counter(int start) {
        count = start;
    }

    int value() { return count; }

    void increment() { count = count + 1; }

private:
    int count = 0;
};

class Radio {
public:
    Radio(double startMhz) {
        mhz = 88.0;
        tune(startMhz);
    }

    double frequency() { return mhz; }

    void tune(double newMhz) {
        if (newMhz >= 88.0 && newMhz <= 108.0) {
            mhz = newMhz;
        }
    }

private:
    double mhz;
};
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
