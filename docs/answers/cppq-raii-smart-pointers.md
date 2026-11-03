## RAII and Smart Pointers

*cppq-raii-smart-pointers · medium*

**Goal.** Write classes whose constructors and destructors log to a global `g_events` list, and functions that create, move and share `unique_ptr` / `shared_ptr` objects, including a `unique_ptr` linked list.

**You need to know.**

- RAII: acquire in the constructor, release in the destructor, which runs at the closing `}` (README RAII section).
- `std::make_unique`, `std::make_shared`, `use_count()`.
- A `unique_ptr` cannot be copied, only moved with `std::move`.
- `.get()` gives a raw, non-owning pointer.

**Walkthrough.**

1. Run `./check`. Then add the includes and the shared event log. The tests read `g_events` but nobody defines it for you.

   ```cpp
   #include <memory>
   #include <string>
   #include <vector>
   inline std::vector<std::string> g_events;
   ```

2. Task 1, unique pointer. When the `unique_ptr` leaves its scope it deletes the `Widget`, so the destructor logs `"broken"`.

   ```cpp
   class Widget {
   public:
       Widget() { g_events.push_back("built"); }
       ~Widget() { g_events.push_back("broken"); }
   };
   inline std::unique_ptr<Widget> makeWidget() { return std::make_unique<Widget>(); }
   ```

3. Task 2, moving ownership. Taking the parameter by value means the caller has to `std::move` in, which leaves the caller's pointer null (the test checks that).

   ```cpp
   inline int takeOwnership(std::unique_ptr<int> p) { return *p; }
   ```

4. Task 3, shared counting. Inside the inner scope two `shared_ptr`s own the int, so `use_count()` is 2.

   ```cpp
   inline long sharedCountDemo() {
       auto p1 = std::make_shared<int>(100);
       long inside = 0;
       {
           auto p2 = p1;
           inside = p1.use_count();
       }
       return inside;
   }
   ```

5. Task 4, scope logger. Same idea as `Widget`, with the name in the message.

   ```cpp
   class ScopeLogger {
   public:
       explicit ScopeLogger(std::string name) : name_(std::move(name)) { g_events.push_back("Enter: " + name_); }
       ~ScopeLogger() { g_events.push_back("Exit: " + name_); }
   private:
       std::string name_;
   };
   ```

6. Task 5, smart factory.

   ```cpp
   inline std::unique_ptr<int> createObject(int value) { return std::make_unique<int>(value); }
   ```

7. Task 6, linked list. Build from the back so each new node can take ownership of the chain built so far. `traverse` walks with raw pointers because it only reads.

   ```cpp
   struct Node { int data; std::unique_ptr<Node> next; };

   inline std::unique_ptr<Node> makeChain(const std::vector<int>& values) {
       std::unique_ptr<Node> head;
       for (auto it = values.rbegin(); it != values.rend(); ++it)
           head = std::make_unique<Node>(Node{*it, std::move(head)});
       return head;
   }
   inline std::vector<int> traverse(const Node* node) {
       std::vector<int> out;
       for (; node; node = node->next.get()) out.push_back(node->data);
       return out;
   }
   ```

8. Task 7, resource manager. A fake file handle that "opens" and "closes" through `g_events`.

   ```cpp
   class FileManager {
   public:
       explicit FileManager(std::string name) : name_(std::move(name)) { g_events.push_back("Opening " + name_); }
       ~FileManager() { g_events.push_back("Closing " + name_); }
       void write(const std::string& msg) { g_events.push_back(msg); }
   private:
       std::string name_;
   };
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Forgetting `inline std::vector<std::string> g_events;`, so nothing compiles.
- Taking the parameter as `std::unique_ptr<int>&` in Task 2: the caller's pointer is then not emptied and the `ptr == nullptr` check fails.
- Building the list front to back and losing the head, or getting the values in reverse order.
