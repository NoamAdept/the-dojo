// Task 7: producer/consumer SafeQueue
#include "check.h"
#include "tasks.h"
int main() {
    SafeQueue<int> q;
    long sum = 0;
    std::thread consumer([&] { for (int i = 0; i < 1000; ++i) sum += q.pop(); });
    std::thread producer([&] { for (int i = 1; i <= 1000; ++i) q.push(i); });
    producer.join();
    consumer.join();
    EXPECT(sum == 500500 && q.size() == 0);
}
