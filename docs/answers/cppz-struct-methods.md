## Structs That Do Things

*cppz-struct-methods · easy*

**Goal.** Give the `Rectangle` struct in `tasks.h` four member functions (`area`, `perimeter`, `scale`, `isSquare`) and finish the free function `makeSquare`.

**You need to know.**

- A struct groups fields (`width`, `height`) and can hold functions too, called methods (README lesson).
- Inside a method you use the field names directly; `r.area()` works on `r`'s own fields.
- A method can change the fields of the object it is called on.
- Brace initialisation: `Rectangle r{2.0, 5.0};` sets width then height.

**Walkthrough.**

1. Task 1, `area` inside the struct:

   ```cpp
   double area() { return width * height; }
   ```

   `width` and `height` here mean the fields of whichever rectangle the method was called on.

2. Task 2, `perimeter`:

   ```cpp
   double perimeter() { return 2 * (width + height); }
   ```

   The parentheses make the addition happen before the multiplication.

3. Task 3, `scale`:

   ```cpp
   void scale(double factor) {
       width = width * factor;
       height = height * factor;
   }
   ```

   Assigning to the fields changes this rectangle only; other rectangles keep their own values.

4. Task 4, `isSquare`:

   ```cpp
   bool isSquare() { return width == height; }
   ```

   The comparison already is the true or false answer.

5. Task 5, `makeSquare` (outside the struct):

   ```cpp
   Rectangle makeSquare(double side) {
       Rectangle r{side, side};
       return r;
   }
   ```

   The braces fill `width` then `height` in the order they are declared, and the new rectangle is returned as a value.

6. Run `./check`.

**Check.** `./check` prints `5/5 tasks pass` and then `CHECK_OK`.

**Common mistakes.**

- Writing `return 2 * width + height;` for the perimeter (missing parentheses), which gives 9 instead of 13 for a 2.5 by 4 rectangle.
- Making `scale` return a new value instead of changing the fields. The test checks `r.width` and `r.height` after the call.
- Writing `Rectangle.width` or `this.width`. Inside a method the field name alone is enough.
