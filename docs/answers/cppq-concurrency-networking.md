## Concurrency and Networking

*cppq-concurrency-networking · hard*

**Goal.** Write thread code in `tasks.h` (a data race, a mutex fix, an atomic, a parallel sum and a blocking thread-safe queue) plus two socket helpers: building a `sockaddr_in` and a TCP "ping" on localhost.

**You need to know.**

- `std::thread`, `join()`, `std::mutex` with `std::lock_guard`, and `std::atomic<int>` (README concurrency part).
- `std::ref` is needed to pass a reference into a thread function.
- `std::condition_variable::wait(lock, predicate)` for a blocking pop.
- `socket`, `connect`, `htons`, `inet_pton` (README networking part). The tests only use 127.0.0.1.

**Walkthrough.**

1. Run `./check`. The starter already has every include, and `check.py` adds `-pthread`.

2. Task 1, racer. Both threads read and write `counter` with no lock, so updates get lost (any result from 1 to 200000 passes). The locked version is always exact.

   ```cpp
   inline int racyCount(int perThread) {
       int counter = 0;
       auto work = [&] { for (int i = 0; i < perThread; ++i) { int v = counter; counter = v + 1; } };
       std::thread a(work), b(work);
       a.join(); b.join();
       return counter;
   }
   inline int lockedCount(int perThread) {
       int counter = 0;
       std::mutex m;
       auto work = [&] {
           for (int i = 0; i < perThread; ++i) { std::lock_guard<std::mutex> lock(m); ++counter; }
       };
       std::thread a(work), b(work);
       a.join(); b.join();
       return counter;
   }
   ```

3. Task 2, atomic counter. `fetch_add` is one indivisible step, so no mutex is needed.

   ```cpp
   inline int atomicCount(int perThread) {
       std::atomic<int> counter{0};
       auto work = [&] { for (int i = 0; i < perThread; ++i) counter.fetch_add(1); };
       std::thread a(work), b(work);
       a.join(); b.join();
       return counter.load();
   }
   ```

4. Task 3, sleepy thread. `join()` waits for the sleep to finish, so the call takes at least `ms`.

   ```cpp
   inline std::vector<std::string> sleepyThread(int ms) {
       std::vector<std::string> events;
       std::thread t([&] {
           events.push_back("Start");
           std::this_thread::sleep_for(std::chrono::milliseconds(ms));
           events.push_back("End");
       });
       t.join();
       return events;
   }
   ```

5. Task 4, network address. Ports and addresses go on the wire in big-endian, which `htons` and `inet_pton` take care of.

   ```cpp
   inline sockaddr_in makeAddress(const char* ip, uint16_t port) {
       sockaddr_in a{};
       a.sin_family = AF_INET;
       a.sin_port = htons(port);
       inet_pton(AF_INET, ip, &a.sin_addr);
       return a;
   }
   ```

6. Task 5, parallel sum. Each thread writes its own result variable; `std::ref` passes it by reference. Split at `n / 2` so odd `n` (1001) still covers every number once.

   ```cpp
   inline void sumRange(int from, int to, long& out) {
       out = 0;
       for (int i = from; i <= to; ++i) out += i;
   }
   inline long parallelSum(int n) {
       long lo = 0, hi = 0;
       std::thread a(sumRange, 1, n / 2, std::ref(lo));
       std::thread b(sumRange, n / 2 + 1, n, std::ref(hi));
       a.join(); b.join();
       return lo + hi;
   }
   ```

7. Task 6, port pinger. `connect()` returns 0 only if something is listening. Always `close` the socket.

   ```cpp
   inline bool ping(const char* ip, uint16_t port) {
       int fd = socket(AF_INET, SOCK_STREAM, 0);
       if (fd < 0) return false;
       sockaddr_in a = makeAddress(ip, port);
       bool up = connect(fd, reinterpret_cast<sockaddr*>(&a), sizeof a) == 0;
       close(fd);
       return up;
   }
   ```

8. Task 7, thread-safe queue. `pop` sleeps on the condition variable until the queue is not empty; `push` wakes it. The predicate form also handles spurious wake-ups. `size()` is const, so the mutex is `mutable`.

   ```cpp
   template <class T>
   class SafeQueue {
   public:
       void push(T value) {
           { std::lock_guard<std::mutex> lock(m_); q_.push(std::move(value)); }
           cv_.notify_one();
       }
       T pop() {
           std::unique_lock<std::mutex> lock(m_);
           cv_.wait(lock, [&] { return !q_.empty(); });
           T value = std::move(q_.front());
           q_.pop();
           return value;
       }
       std::size_t size() const { std::lock_guard<std::mutex> lock(m_); return q_.size(); }
   private:
       mutable std::mutex m_;
       std::condition_variable cv_;
       std::queue<T> q_;
   };
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Passing `lo` without `std::ref` in Task 5: it does not compile, because `std::thread` copies its arguments.
- Using `if (q_.empty()) cv_.wait(lock)` without the predicate, or forgetting `notify_one`: the consumer hangs and `./check` reports "timed out".
- Forgetting `htons` on the port: the test reads it back with `ntohs` and gets a different number.
