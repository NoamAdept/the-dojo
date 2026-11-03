## Parse Length-Prefixed Records

*cpp-binary-parser · medium*

**Goal.** Write `parse_records` in `records.cpp` so it walks a buffer of type/length/payload records, calls a visitor for each complete one and refuses truncated input, then write `count_records` using your own visitor.

**You need to know.**

- The record format from the README: 1 type byte, 1 length byte, then `length` payload bytes.
- Walking a buffer with an `offset` and checking the remaining bytes before every read.
- Callbacks with a `void*` context (from cpp-function-pointers).
- Why `size - offset` is safe when `offset <= size`, and `offset + n` is not.

**Walkthrough.**

All code goes in `records.cpp`. Delete the two `// TODO task` lines in `parse_records` and the one in `count_records` as you go. Do not change `records.hpp`.

1. Task 1: the basic walk.

   ```cpp
   std::size_t offset = 0;
   while (offset < size) {
       uint8_t type = data[offset];
       std::size_t length = data[offset + 1];
       offset += 2;
       visit(type, data + offset, length, context);
       offset += length;
   }
   return true;
   ```

   `data + offset` points at the payload, and moving `offset` by the length lands on the next header. An empty buffer never enters the loop, so it returns true.

2. Task 2: add the two safety checks inside the loop. The final function:

   ```cpp
   bool parse_records(const uint8_t* data, std::size_t size, record_visitor visit, void* context)
   {
       std::size_t offset = 0;
       while (offset < size) {
           if (size - offset < 2) {
               return false;
           }
           uint8_t type = data[offset];
           std::size_t length = data[offset + 1];
           offset += 2;
           if (length > size - offset) {
               return false;
           }
           visit(type, data + offset, length, context);
           offset += length;
       }
       return true;
   }
   ```

   The first check makes sure a whole 2-byte header is there before reading it. The second makes sure the whole payload is there before calling `visit`, so a broken record is never visited.

3. Task 3: a counting visitor plus `count_records`. Put the visitor above `count_records`.

   ```cpp
   void count_one(uint8_t, const uint8_t*, std::size_t, void* context)
   {
       int* n = static_cast<int*>(context);
       *n += 1;
   }

   int count_records(const uint8_t* data, std::size_t size)
   {
       int n = 0;
       if (!parse_records(data, size, count_one, &n)) {
           return -1;
       }
       return n;
   }
   ```

   The parameters are left unnamed so `-Wextra` does not complain they are unused. `&n` is the context, so the visitor adds 1 to the caller's counter.

**Check.** `./check` prints `3/3 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Checking `offset + 2 > size` or `offset + length > size` instead of comparing against `size - offset`: it works on small tests but is the overflow pattern the module warns about.
- Forgetting to skip the 2 header bytes before using `data + offset` as the payload.
- Calling `visit` before the length check: the test `02 04 01` must show `false 0`, not one visited record.
