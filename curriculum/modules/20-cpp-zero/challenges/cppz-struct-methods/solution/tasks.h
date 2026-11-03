// C++ Toolbox 4: structs that do things.
#pragma once

struct Rectangle {
    double width;
    double height;

    double area() { return width * height; }

    double perimeter() { return 2 * (width + height); }

    void scale(double factor) {
        width = width * factor;
        height = height * factor;
    }

    bool isSquare() { return width == height; }
};

Rectangle makeSquare(double side) {
    Rectangle r{side, side};
    return r;
}
