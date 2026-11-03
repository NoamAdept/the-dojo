// C++ Toolbox 5: classes, private data and constructors.
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
