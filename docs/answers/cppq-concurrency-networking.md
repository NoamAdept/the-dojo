# Concurrency and Networking

`cppq-concurrency-networking` · Orange Belt

**Goal:** Write thread code in `tasks.h` (a data race, a mutex fix, an atomic, a parallel sum and a blocking thread-safe queue) plus two socket helpers: building a `sockaddr_in` and a TCP "ping" on localhost.

**File `tasks.h`**

```cpp
#pragma once
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <vector>

inline int racyCount(int perThread) {
    int counter = 0;
    auto work = [&] {
        for (int i = 0; i < perThread; ++i) {
            int v = counter;  // deliberately racy read-modify-write
            counter = v + 1;
        }
    };
    std::thread a(work), b(work);
    a.join();
    b.join();
    return counter;
}

inline int lockedCount(int perThread) {
    int counter = 0;
    std::mutex m;
    auto work = [&] {
        for (int i = 0; i < perThread; ++i) {
            std::lock_guard<std::mutex> lock(m);
            ++counter;
        }
    };
    std::thread a(work), b(work);
    a.join();
    b.join();
    return counter;
}

inline int atomicCount(int perThread) {
    std::atomic<int> counter{0};
    auto work = [&] {
        for (int i = 0; i < perThread; ++i) counter.fetch_add(1);
    };
    std::thread a(work), b(work);
    a.join();
    b.join();
    return counter.load();
}

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

inline sockaddr_in makeAddress(const char* ip, uint16_t port) {
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(port);
    inet_pton(AF_INET, ip, &a.sin_addr);
    return a;
}

inline void sumRange(int from, int to, long& out) {
    out = 0;
    for (int i = from; i <= to; ++i) out += i;
}

inline long parallelSum(int n) {
    long lo = 0, hi = 0;
    std::thread a(sumRange, 1, n / 2, std::ref(lo));
    std::thread b(sumRange, n / 2 + 1, n, std::ref(hi));
    a.join();
    b.join();
    return lo + hi;
}

inline bool ping(const char* ip, uint16_t port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) return false;
    sockaddr_in a = makeAddress(ip, port);
    bool up = connect(fd, reinterpret_cast<sockaddr*>(&a), sizeof a) == 0;
    close(fd);
    return up;
}

template <class T>
class SafeQueue {
public:
    void push(T value) {
        {
            std::lock_guard<std::mutex> lock(m_);
            q_.push(std::move(value));
        }
        cv_.notify_one();
    }
    T pop() {
        std::unique_lock<std::mutex> lock(m_);
        cv_.wait(lock, [&] { return !q_.empty(); });
        T value = std::move(q_.front());
        q_.pop();
        return value;
    }
    std::size_t size() const {
        std::lock_guard<std::mutex> lock(m_);
        return q_.size();
    }

private:
    mutable std::mutex m_;
    std::condition_variable cv_;
    std::queue<T> q_;
};
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
