// C++ Toolbox 5: classes, private data and constructors.
#pragma once

class Counter {
public:
    // Task 1: store start in count.
    Counter(int start) {
        // write your code here
    }

    // Task 1: return count.
    int value() {
        return -1;  // replace this line
    }

    // Task 2: add 1 to count.
    void increment() {
        // write your code here
    }

    // Task 3: put a private: label on the line above count.
    int count = 0;
};

class Radio {
public:
    // Task 4: store startMhz. Task 5: use 88.0 if startMhz is not in 88.0..108.0.
    Radio(double startMhz) {
        // write your code here
    }

    // Task 4: return the frequency.
    double frequency() {
        return 0;  // replace this line
    }

    // Task 4: change the frequency. Task 5: ignore values outside 88.0..108.0.
    void tune(double newMhz) {
        // write your code here
    }

    // Task 4: add a private: label and a double field for the frequency here.
};
