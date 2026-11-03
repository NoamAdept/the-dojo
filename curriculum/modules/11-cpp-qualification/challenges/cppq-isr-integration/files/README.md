# Interrupt Service Routines

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

Linux user space (normal programs) has no hardware interrupts. So the tasks simulate (copy the behavior of) interrupts with plain function calls. Task 7 uses a real POSIX signal.

## Interrupt Service Routines (ISR) Integration in C++

Welcome to Module 18! This module connects software and hardware.

An **Interrupt** is a signal from hardware, for example a timer, a button, or a UART (a serial port). The interrupt pauses the main code. Then the CPU jumps to a special function: the **ISR**.

**The Golden Rules of ISRs:**
1.  **Keep it Short**: Do the smallest amount of work (set a flag, copy a byte). Then exit.
2.  **No Blocking**: Never call `sleep` or `printf`. Never wait for a mutex.
3.  **No Allocation**: Do not use `new` / `malloc`. They are not re-entrant (not safe if an interrupt happens while they run).

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **C-linkage skeleton**: declare `extern "C" void ADC_IRQHandler();`. It adds 1 to `volatile int g_adcIrqCount`.
2. **Flag**: write `volatile bool conversionDone = false;` and `void ADC_ISR()`. The function sets the flag.
3. **Class handler**: `Motor` has a static `emergencyStop()`. It sets the static `Motor::stopped` flag. `void Button_ISR()` calls it.
4. **Button debounce**: write `bool EXTI_ISR(int currentTimeMs)`.
   - It accepts a press only if at least 50 ms passed since the last accepted press.
   - Keep the time of the last press in a static `lastTime`. It starts at -1000.
   - It returns true if it accepted the press.
   - Also write `void resetDebounce()`.
5. **Ring buffer**: `struct RingBuffer` holds 16 `uint8_t` slots, with volatile `head` and `tail`.
   - `bool push(uint8_t)` returns false when the buffer is full. It holds 15 items at most, because it keeps 1 slot empty.
   - `bool pop(uint8_t&)` returns false when the buffer is empty.
6. **Dispatcher**: `InterruptManager` has a static `registerCallback(void (*cb)())`. Also write `void Global_ISR()`. It calls the callback only if one is registered.
7. **Real signal**: `void installSignalIsr(int signo)` installs a `sigaction` handler. The handler sets `volatile std::sig_atomic_t g_signalSeen = 1`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
