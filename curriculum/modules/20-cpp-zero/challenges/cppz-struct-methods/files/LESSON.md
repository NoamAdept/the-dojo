# Structs That Do Things: lesson

### A struct groups values

A rectangle has a width and a height. You could keep 2 separate variables. But they belong together. A **struct** lets you make a new type. This type holds several named variables together. These variables are called **fields**:

```cpp
struct Rectangle {
    double width;
    double height;
};                                 // note the ; after the }

Rectangle r;                       // r is one Rectangle
r.width = 3.0;                     // reach a field with a dot
r.height = 4.0;
std::cout << r.width * r.height << std::endl;   // 12
```

`Rectangle` is now a type, like `int` or `std::string`. `r` is a variable of that type. One value of a struct type is called an **object**.

### Functions inside a struct

You can also put functions **inside** the struct:

```cpp
struct Rectangle {
    double width;
    double height;

    double area() {
        return width * height;     // the fields are used directly by name
    }
};

Rectangle r{3.0, 4.0};             // width 3, height 4 (fields in order)
std::cout << r.area() << std::endl; // 12
```

A function inside a struct is a **member function**. Another name for it is a **method**. You call it with a dot, like `r.area()`. This is the same way you called `text.size()` on a string. Inside the method, `width` and `height` are the fields of the object you called it on. If you call it on another rectangle, it uses the fields of that rectangle.

`Rectangle r{3.0, 4.0};` makes a Rectangle. It fills the fields in the same order as they are written in the struct. You can also set the fields one at a time: `r.width = 3.0;`.

### Methods can change the object

A method can change the fields of the object it was called on:

```cpp
struct Counter {
    int count;
    void bump() { count = count + 1; }
};

Counter c{0};
c.bump();
c.bump();          // c.count is now 2
```

### Returning a struct

A normal function (outside the struct) can build a struct and return it:

```cpp
Rectangle makeWide(double h) {
    Rectangle r{h * 2, h};
    return r;
}
```

### New words

- **struct**: a new type that holds several named fields together.
- **member function / method**: a function inside a struct. You call it with a dot: `r.area()`.
- **object**: one value of a struct type, for example the `r` in `Rectangle r{3.0, 4.0};`.
- **field**: a variable inside a struct (`width`, `height`). Also called a member variable.
- **brace initialisation**: `Rectangle r{3.0, 4.0};` fills the fields in order.
