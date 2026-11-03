# Concurrency and Networking: lesson

### 1. Threads & Concurrency (`std::thread`)

A **Thread** is an independent sequence of execution. This means it runs its own code, at the same time as other threads. Concurrency means doing several things at the same time.

You get `std::thread` from the header `<thread>`.

```cpp
#include <iostream>
#include <thread>

void task() {
    std::cout << "Hello from Thread!" << std::endl;
}

int main() {
    std::thread t(task);
    std::cout << "Hello from Main!" << std::endl;
    t.join(); // Wait for thread to finish
    return 0;
}
```

`t.join()` makes `main` wait until the thread is finished. Always join a thread before it is destroyed.

### 2. Data Races & Mutexes

Sometimes two threads write to the same memory at the same time. This is a **Data Race**. It corrupts (damages) your data. For example, a counter can lose some of its updates.

Use `std::mutex` to protect shared data. A mutex is a lock. Only 1 thread can hold it at a time.

```cpp
#include <iostream>
#include <thread>
#include <mutex>

int counter = 0;
std::mutex mtx;

void increment() {
    for(int i=0; i<10000; ++i) {
        std::lock_guard<std::mutex> lock(mtx); // RAII Lock
        counter++;
    }
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    t1.join();
    t2.join();
    std::cout << "Final: " << counter << std::endl;
    return 0;
}
```

`std::lock_guard` locks the mutex when it is created. It unlocks the mutex when it goes out of scope. This is RAII (the object cleans up by itself when it is destroyed).

### 3. Atomics

An atomic operation happens as one step. No other thread can see it half-done. For simple counters or flags, `std::atomic` is faster and simpler than a mutex.

```cpp
#include <atomic>
#include <iostream>
#include <thread>

std::atomic<int> safeCounter(0);

void fastInc() {
    for(int i=0; i<10000; ++i) safeCounter++;
}

int main() {
    std::thread t1(fastInc);
    std::thread t2(fastInc);
    t1.join(); 
    t2.join();
    std::cout << "Atomic: " << safeCounter << std::endl;
    return 0;
}
```

### 4. Networking with Sockets

Networking often uses **Blocking I/O**. "Blocking" means the call waits until data arrives. Because of this, we often put network code in separate threads. Then the rest of the program does not have to wait.

**Sockets** are the standard API for TCP/UDP. A socket is one end of a network connection. TCP and UDP are the 2 main ways to send data over a network.

```cpp
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

int main() {
    // 1. Create Socket (IPv4, TCP)
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return 1;

    // 2. Define Address (example.com IP: 93.184.216.34, Port 80)
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(80);
    inet_pton(AF_INET, "93.184.216.34", &serv_addr.sin_addr);

    // 3. Connect (This blocks!)
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == 0) {
        std::cout << "Connected to example.com!" << std::endl;
    } else {
        std::cerr << "Connection Failed" << std::endl;
    }

    // 4. Close
    close(sock);
    return 0;
}
```

The steps are:

1. Create a socket with `socket()`.
2. Fill in the address (`sockaddr_in`). `htons` puts the port number in network byte order. `inet_pton` turns an IP text like `"93.184.216.34"` into binary form.
3. Connect with `connect()`. It returns `0` when the connection works.
4. Close the socket with `close()`.

---

## New words

- **thread**: one path of running code. A program can have many threads at the same time.
- **data race**: 2 threads use the same memory at the same time, and at least 1 of them writes.
- **mutex**: a lock. Only 1 thread can hold it at a time.
- **atomic**: an operation that happens in one step that no other thread can interrupt.
- **condition variable** (`std::condition_variable`): lets a thread sleep until another thread tells it there is work.
- **socket**: one end of a network connection. On Linux it is a file descriptor (a small number for an open file or connection).
- **blocking**: a call that waits until it is finished before your code can continue.

## Offline help

- Offline: `man 2 socket`
