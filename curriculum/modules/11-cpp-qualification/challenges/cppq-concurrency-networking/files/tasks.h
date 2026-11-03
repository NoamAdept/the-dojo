// C++ Qualification 14: concurrency and networking.
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

// Task 1: int racyCount(int perThread); int lockedCount(int perThread)
// Task 2: int atomicCount(int perThread)
// Task 3: std::vector<std::string> sleepyThread(int ms)
// Task 4: sockaddr_in makeAddress(const char* ip, uint16_t port)
// Task 5: long parallelSum(int n)
// Task 6: bool ping(const char* ip, uint16_t port)
// Task 7: template <class T> class SafeQueue
