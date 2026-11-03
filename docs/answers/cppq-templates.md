## Templates and Generic Programming

*cppq-templates · medium*

**Goal.** Write function templates (`mySwap`, `add`, `printTriplet`, `myMax`) and class templates (`Holder<T>`, `MyPair<K, V>`, `Stack<T>`) in `tasks.h` that work for ints, doubles and strings.

**You need to know.**

- `template <class T>` before a function or class; the compiler deduces `T` from arguments.
- Templates live entirely in the header.
- `std::ostringstream` turns any printable type into a string.
- Throwing `std::out_of_range` from `<stdexcept>`.

**Walkthrough.**

1. Run `./check`. The starter already includes `<sstream>`, `<stdexcept>`, `<string>` and `<vector>`; add `<utility>` for `std::move`.

2. Task 1, generic swap. Moving avoids copying big objects like strings.

   ```cpp
   template <class T>
   void mySwap(T& a, T& b) {
       T tmp = std::move(a);
       a = std::move(b);
       b = std::move(tmp);
   }
   ```

3. Task 2, generic adder. `+` means addition for ints and concatenation for strings.

   ```cpp
   template <class T>
   T add(T a, T b) { return a + b; }
   ```

4. Task 3, Holder. `display()` streams the content, so it works for any type with `<<`.

   ```cpp
   template <class T>
   class Holder {
   public:
       explicit Holder(T content) : content_(std::move(content)) {}
       const T& get() const { return content_; }
       std::string display() const {
           std::ostringstream out;
           out << content_;
           return out.str();
       }
   private:
       T content_;
   };
   ```

5. Task 4, three type parameters, one per argument.

   ```cpp
   template <class A, class B, class C>
   std::string printTriplet(A a, B b, C c) {
       std::ostringstream out;
       out << "(" << a << ", " << b << ", " << c << ")";
       return out.str();
   }
   ```

6. Task 5, max finder. Returns a reference to whichever argument is larger.

   ```cpp
   template <class T>
   const T& myMax(const T& a, const T& b) { return a > b ? a : b; }
   ```

7. Task 6, generic pair. Members are public because the test reads `a.key` and `a.value`.

   ```cpp
   template <class K, class V>
   struct MyPair {
       K key;
       V value;
       MyPair(K k, V v) : key(std::move(k)), value(std::move(v)) {}
       std::string print() const {
           std::ostringstream out;
           out << "Key: " << key << ", Value: " << value;
           return out.str();
       }
   };
   ```

8. Task 7, generic stack. A `vector` does the storage; `back()` is the top. Guard both `top` and `pop`, because `back()` on an empty vector is undefined behaviour, not an exception.

   ```cpp
   template <class T>
   class Stack {
   public:
       void push(T val) { items_.push_back(std::move(val)); }
       void pop() {
           if (items_.empty()) throw std::out_of_range("pop on empty stack");
           items_.pop_back();
       }
       const T& top() const {
           if (items_.empty()) throw std::out_of_range("top on empty stack");
           return items_.back();
       }
       bool isEmpty() const { return items_.empty(); }
   private:
       std::vector<T> items_;
   };
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Calling `myMax(3, 9.5)` or `add(1, 2.5)` while experimenting: `T` cannot be both `int` and `double`, so deduction fails. Both arguments must have the same type (or write `myMax<double>(3, 9.5)`).
- Using `std::to_string` in `display()`: it does not accept `std::string`, so `Holder<std::string>` fails to compile.
- Not throwing in `top()` on an empty stack: the test expects `std::out_of_range`.
