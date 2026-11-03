# Interrupt Service Routines: lesson

An **ISR** (Interrupt Service Routine) is a function that runs when hardware sends an interrupt. An interrupt pauses the main program. The CPU then jumps to the ISR. When the ISR is done, the main program continues.

### 1. The `extern "C"` Constraint

A hardware vector table is a list of ISR addresses. The CPU uses it to find the right ISR. These tables are usually linked using C symbols (plain C function names).

C++ mangles function names. "Mangling" means the compiler adds extra characters to each name. So the C name does not match anymore.

To write an ISR in C++, you must stop name mangling. Use `extern "C"`:

```cpp
extern "C" {
    void TIM2_IRQHandler() {
        // Handle Timer 2 Interrupt
    }
}
```

### 2. Shared Data and `volatile`

Sometimes an ISR writes a variable and `main` reads it. Then this variable **must** be `volatile`.

Why? The compiler optimizes your code. It can see that `main` never changes the value. Then it may read the value only once and skip all later reads. `volatile` tells the compiler: "this value can change at any time, so always read it again from memory."

```cpp
#include <iostream>
#include <thread>
#include <chrono>

// Simulated ISR shared variable
volatile bool dataReady = false;

// Simulated ISR
void TIM2_IRQHandler() {
    // Simulate hardware work
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); 
    dataReady = true;
}

int main() {
    // Launch ISR in a thread to simulate async hardware event
    std::thread t(TIM2_IRQHandler);
    
    std::cout << "Waiting for data..." << std::endl;
    
    // If dataReady wasn't volatile, this might hang forever in release mode
    while (!dataReady) {
        // Busy wait
    }
    
    std::cout << "Data received!" << std::endl;
    t.join();
    return 0;
}
```

### 3. Atomic Flags

`volatile` forces the program to read the value each time. But it does not stop **partial writes** for larger types. A partial write means another part of the code sees a value that is only half-written.

For status flags, `std::atomic_flag` (or `std::atomic<bool>`) is safer. An atomic value is always read and written in one step.

```cpp
#include <iostream>
#include <atomic>

std::atomic<bool> btnPressed(false);

void EXTI0_IRQHandler() {
    btnPressed.store(true);
}

int main() {
    EXTI0_IRQHandler(); // Simulate button press
    
    if (btnPressed.load()) {
        std::cout << "Button was pressed!" << std::endl;
        btnPressed.store(false); // Clear flag
    }
    return 0;
}
```

### 4. Static Class Methods as ISRs

You cannot use a normal member function as an ISR. A member function needs a hidden `this` pointer (a pointer to the object). The hardware cannot give it one.

You **can** use a `static` member function. A static function belongs to the class, not to one object. So it needs no `this` pointer.

```cpp
#include <iostream>

class UART {
public:
    static void rxInterrupt() {
        std::cout << "Byte received in static ISR" << std::endl;
        // Note: Cannot access non-static 'this->buffer' directly here!
    }
};

extern "C" {
    void UART_IRQHandler() {
        UART::rxInterrupt();
    }
}

int main() {
    UART_IRQHandler();
    return 0;
}
```

### 5. Connecting ISR to Objects (Singleton/Global)

Sometimes the ISR must change one specific object. Then the ISR needs a way to find this object. Usually you use a global pointer, or a Singleton instance that the ISR can reach. (A Singleton is a class that has only 1 object in the whole program.)

```cpp
#include <iostream>

class LEDController {
public:
    void toggle() { std::cout << "LED Toggled" << std::endl; }
};

// Data Segment Global
LEDController myLed;

extern "C" {
    void TIMER_ISR() {
        myLed.toggle(); // Access global object
    }
}

int main() {
    TIMER_ISR();
    return 0;
}
```

---

## New words

- **interrupt**: a signal from hardware that pauses the main program.
- **ISR** (Interrupt Service Routine): the function that runs when an interrupt happens.
- **vector table**: a list that tells the CPU which ISR to run for each interrupt.
- **name mangling**: the C++ compiler changes function names to add type information.
- **`volatile`**: tells the compiler that a value can change at any time, so it must always read it again.
- **atomic**: read or written in one step, so no one sees a half-written value.
- **re-entrant**: safe to call again while an earlier call is still running.
