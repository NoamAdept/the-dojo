## Pointers and References

*cppq-pointers-references · easy*

**Goal.** Write seven small functions in `tasks.h` that take addresses, read and write through pointers, and walk arrays and C strings with pointer arithmetic.

**You need to know.**

- `&x` gives an address, `*p` reads or writes what `p` points at (README pointer basics).
- A reference parameter (`int&`) is another name for the caller's variable.
- `++p` moves a pointer to the next element; a C string ends at `'\0'`.
- Always check for `nullptr` before dereferencing.

**Walkthrough.**

1. Run `./check`, then add `#include <string>` to `tasks.h`.

2. Task 1, address-of. `v` is a reference, so `&v` is the caller's variable's address.

   ```cpp
   inline int* addressOf(int& v) { return &v; }
   ```

3. Task 2, modify via pointer. `*p *= 2` changes the original variable.

   ```cpp
   inline void doubleViaPointer(int* p) { *p *= 2; }
   ```

4. Task 3, walk a C string. Move a pointer forward until it hits the terminator. The test reads `tasks.h` and fails if it finds `strlen(` anywhere in it, even in a comment.

   ```cpp
   inline std::string walkCString(const char* s) {
       std::string out;
       for (const char* p = s; *p != '\0'; ++p) out += *p;
       return out;
   }
   ```

5. Task 4, null check. Test for null first, then dereference.

   ```cpp
   inline std::string describe(const int* p) {
       if (p == nullptr) return "Null Pointer";
       return "Value is: " + std::to_string(*p);
   }
   ```

6. Task 5, swapper. A temporary holds one value while the other is copied over.

   ```cpp
   inline void swap(int* a, int* b) {
       int tmp = *a;
       *a = *b;
       *b = tmp;
   }
   ```

7. Task 6, array reverser. Two pointers start at both ends and meet in the middle. `start < end` stops correctly for odd, even and zero sizes (with size 0, `end` is before `start`, so the loop never runs).

   ```cpp
   inline void reverseArray(int* arr, int size) {
       for (int *start = arr, *end = arr + size - 1; start < end; ++start, --end) swap(start, end);
   }
   ```

8. Task 7, min and max in one pass. Seed both with the first element, then compare each later element once. The results go out through the two pointer parameters.

   ```cpp
   inline void findMinMax(const int* arr, int size, int* minOut, int* maxOut) {
       *minOut = *maxOut = arr[0];
       for (const int* p = arr + 1; p < arr + size; ++p) {
           if (*p < *minOut) *minOut = *p;
           if (*p > *maxOut) *maxOut = *p;
       }
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `strlen` in a comment or using `std::string(s)` in Task 3: the test scans the source text, and the README forbids the shortcut.
- Seeding min and max with 0: the one-element test `{42}` then reports min 0.
- Using `start != end` in the reverser: on an even-length array the pointers cross and never become equal.
