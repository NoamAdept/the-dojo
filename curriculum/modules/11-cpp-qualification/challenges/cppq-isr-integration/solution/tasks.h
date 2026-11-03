// C++ Qualification 15: ISR integration (simulated on Linux).
#pragma once
#include <atomic>
#include <csignal>
#include <cstdint>

inline volatile int g_adcIrqCount = 0;
extern "C" inline void ADC_IRQHandler() { g_adcIrqCount = g_adcIrqCount + 1; }

inline volatile bool conversionDone = false;
inline void ADC_ISR() { conversionDone = true; }

class Motor {
public:
    static void emergencyStop() { stopped = true; }
    static inline volatile bool stopped = false;
};
inline void Button_ISR() { Motor::emergencyStop(); }

inline int& debounceLastTime() {
    static int lastTime = -1000;
    return lastTime;
}
inline void resetDebounce() { debounceLastTime() = -1000; }
inline bool EXTI_ISR(int currentTimeMs) {
    if (currentTimeMs - debounceLastTime() < 50) return false;  // bounce
    debounceLastTime() = currentTimeMs;
    return true;
}

// Single producer (ISR) / single consumer (main): each index has one writer.
struct RingBuffer {
    uint8_t buffer[16];
    volatile int head = 0;  // written by push (ISR)
    volatile int tail = 0;  // written by pop (main)

    bool push(uint8_t b) {
        int next = (head + 1) % 16;
        if (next == tail) return false;  // full: one slot stays empty
        buffer[head] = b;
        head = next;
        return true;
    }
    bool pop(uint8_t& b) {
        if (tail == head) return false;
        b = buffer[tail];
        tail = (tail + 1) % 16;
        return true;
    }
};

class InterruptManager {
public:
    static void registerCallback(void (*cb)()) { callback = cb; }
    static inline void (*volatile callback)() = nullptr;
};
inline void Global_ISR() {
    if (auto cb = InterruptManager::callback) cb();
}

inline volatile std::sig_atomic_t g_signalSeen = 0;
extern "C" inline void onSignal(int) { g_signalSeen = 1; }
inline void installSignalIsr(int signo) {
    struct sigaction sa {};
    sa.sa_handler = onSignal;
    sigemptyset(&sa.sa_mask);
    sigaction(signo, &sa, nullptr);
}
