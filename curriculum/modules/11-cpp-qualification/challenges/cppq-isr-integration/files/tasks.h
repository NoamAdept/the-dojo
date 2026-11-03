// C++ Qualification 15: ISR integration (simulated on Linux).
#pragma once
#include <atomic>
#include <csignal>
#include <cstdint>

// Task 1: extern "C" void ADC_IRQHandler(); volatile int g_adcIrqCount
// Task 2: volatile bool conversionDone; void ADC_ISR()
// Task 3: class Motor { static void emergencyStop(); static volatile bool stopped; }; void Button_ISR()
// Task 4: bool EXTI_ISR(int currentTimeMs); void resetDebounce()
// Task 5: struct RingBuffer { bool push(uint8_t); bool pop(uint8_t&); }
// Task 6: class InterruptManager; void Global_ISR()
// Task 7: volatile std::sig_atomic_t g_signalSeen; void installSignalIsr(int signo)
