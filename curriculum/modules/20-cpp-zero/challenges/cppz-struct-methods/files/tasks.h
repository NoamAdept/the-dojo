// C++ Toolbox 4: structs that do things.
#pragma once

struct Rectangle {
    double width;
    double height;

    // Task 1: width times height.
    double area() {
        return 0;  // replace this line
    }

    // Task 2: 2 * (width + height).
    double perimeter() {
        return 0;  // replace this line
    }

    // Task 3: multiply width and height by factor.
    void scale(double factor) {
        // write your code here
    }

    // Task 4: true when width equals height.
    bool isSquare() {
        return false;  // replace this line
    }
};

// Task 5: return a Rectangle with width = side and height = side.
Rectangle makeSquare(double side) {
    Rectangle r{0, 0};  // change this
    return r;
}
