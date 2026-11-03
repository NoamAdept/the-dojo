## Interrupt Service Routines

*cppq-isr-integration · hard*

**Goal.** Write ISR-style code in `tasks.h`, simulated on Linux: a C-linkage handler, volatile flags, a static-member handler, a debounce, a lock-free ring buffer, a callback dispatcher and a real POSIX signal handler.

**You need to know.**

- `extern "C"` gives a function the plain C name that a vector table expects (README C-linkage section).
- Data shared with an ISR must be `volatile`; ISRs take no arguments and return nothing.
- Only static member functions (not normal methods) can be used as plain function pointers.
- `sigaction` installs a signal handler; the handler may only touch `volatile std::sig_atomic_t`.

**Walkthrough.**

1. Run `./check`. The starter already includes `<atomic>`, `<csignal>` and `<cstdint>`. Globals in a header need `inline` (C++17).

2. Task 1, C-linkage skeleton. The test re-declares `extern "C" void ADC_IRQHandler();`, which only compiles if yours has C linkage too. `x = x + 1` avoids the `++` on a volatile that newer standards warn about.

   ```cpp
   inline volatile int g_adcIrqCount = 0;
   extern "C" inline void ADC_IRQHandler() { g_adcIrqCount = g_adcIrqCount + 1; }
   ```

3. Task 2, flag. A `static_assert` in the test checks that `conversionDone` is volatile.

   ```cpp
   inline volatile bool conversionDone = false;
   inline void ADC_ISR() { conversionDone = true; }
   ```

4. Task 3, class handler. A static method has no `this`, so it converts to `void (*)()`. `static inline` lets the member be defined in the class.

   ```cpp
   class Motor {
   public:
       static void emergencyStop() { stopped = true; }
       static inline volatile bool stopped = false;
   };
   inline void Button_ISR() { Motor::emergencyStop(); }
   ```

5. Task 4, debounce. Keep `lastTime` in one place that both functions can reach. A function returning a reference to a function-local static does that. Accept a press only if 50 ms or more have passed.

   ```cpp
   inline int& debounceLastTime() { static int lastTime = -1000; return lastTime; }
   inline void resetDebounce() { debounceLastTime() = -1000; }
   inline bool EXTI_ISR(int currentTimeMs) {
       if (currentTimeMs - debounceLastTime() < 50) return false;
       debounceLastTime() = currentTimeMs;
       return true;
   }
   ```

   The test sequence 100, 110, 200, 249, 250 expects accept, reject, accept, reject, accept.

6. Task 5, ring buffer. "Full" means `head + 1 == tail` (mod 16), so one slot always stays empty and 15 bytes fit. The ISR only writes `head`, main only writes `tail`, so no lock is needed.

   ```cpp
   struct RingBuffer {
       uint8_t buffer[16];
       volatile int head = 0;
       volatile int tail = 0;
       bool push(uint8_t b) {
           int next = (head + 1) % 16;
           if (next == tail) return false;
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
   ```

7. Task 6, dispatcher. Copy the pointer once, then call it only if it is not null. A captureless lambda converts to the same pointer type, which the test uses.

   ```cpp
   class InterruptManager {
   public:
       static void registerCallback(void (*cb)()) { callback = cb; }
       static inline void (*volatile callback)() = nullptr;
   };
   inline void Global_ISR() {
       if (auto cb = InterruptManager::callback) cb();
   }
   ```

8. Task 7, real signal. The test calls `std::raise(SIGUSR1)`; without a handler that would kill the process.

   ```cpp
   inline volatile std::sig_atomic_t g_signalSeen = 0;
   extern "C" inline void onSignal(int) { g_signalSeen = 1; }
   inline void installSignalIsr(int signo) {
       struct sigaction sa {};
       sa.sa_handler = onSignal;
       sigemptyset(&sa.sa_mask);
       sigaction(signo, &sa, nullptr);
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Declaring `void ADC_IRQHandler()` without `extern "C"`: task 1 fails with "conflicting declaration of 'void ADC_IRQHandler()' with 'C' linkage".
- Making the ring buffer full at 16 items: then `head == tail` means both full and empty, and the "pushed == 15" check fails.
- Making `emergencyStop` a normal (non-static) method: `&Motor::emergencyStop` is then a member pointer and will not convert to `void (*)()`.
