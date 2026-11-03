# RAII and Smart Pointers: lesson

### 1. Manual Memory Management

Before Smart Pointers, C++ programmers managed memory by hand. You need to understand this for 2 reasons. First, old (legacy) code still does it. Second, it shows what happens "under the hood" (inside, where you cannot see).

#### 1.1 The C Style (`malloc`, `free`)
These functions come from C. They work on raw bytes.
- `void* malloc(size_t size)`: allocates (reserves) `size` bytes. If it fails, it returns `nullptr`.
- `void* calloc(size_t num, size_t size)`: allocates `num * size` bytes and **sets them all to zero**.
- `void* realloc(void* ptr, size_t new_size)`: changes the size of a memory block you already have. It moves the block if it must.
- `void free(void* ptr)`: gives the memory back (releases it).

**Key Concept**: `malloc` does NOT call constructors. It only gives you raw memory space.

```cpp
#include <iostream>
#include <cstdlib> // valid for malloc/free
#include <cstring> // valid for memset/memcpy

int main() {
    // 1. Allocate space for 5 integers
    int* arr = (int*)malloc(5 * sizeof(int));
    
    if (arr == nullptr) return 1;
    
    // 2. Initialize memory to 0 using memset
    // memset(pointer, value, number_of_bytes)
    std::memset(arr, 0, 5 * sizeof(int));
    
    std::cout << "First element: " << arr[0] << std::endl;
    
    // 3. Resize to hold 10 integers (realloc might move the block)
    int* resized = (int*)realloc(arr, 10 * sizeof(int));
    if (resized) {
        arr = resized;
    }
    
    // 4. Free the memory
    free(arr);
    return 0;
}
```

#### 1.2 The C++ Style (`new`, `delete`)
C++ added operators that know about objects.
- `new Type`: allocates memory AND calls the **Constructor**.
- `delete ptr`: calls the **Destructor** AND releases the memory.
- `new Type[]`: allocates an array.
- `delete[] ptr`: releases an array. You must use the `[]` here!

**Compare**: `new` is safer than `malloc`. It makes sure that objects are initialized (set up) correctly.

### 2. What is RAII?

**RAII** stands for **Resource Acquisition Is Initialization**.

The name is long, but the idea is simple:
- **Acquire resources** (memory, files, locks) in the **Constructor**.
- **Release resources** in the **Destructor**.

C++ calls destructors *automatically* when an object goes out of scope. This happens even when an error occurs. So your resources are always cleaned up fully.

Smart pointers are the perfect example of RAII.

```cpp
#include <iostream>

class Wrapper {
public:
    Wrapper() { std::cout << "Resource Acquired" << std::endl; }
    ~Wrapper() { std::cout << "Resource Released" << std::endl; }
};

int main() {
    {
        Wrapper w;
        // Do stuff...
    } // w is destroyed here automatically
    
    std::cout << "Scope ended." << std::endl;
    return 0;
}
```

### 3. Smart Pointers Intro

Smart pointers act like normal pointers. You can use `*` and `->` with them. But they also delete the object they point to automatically, when nobody needs it any more.

They are in `<memory>`.

### 4. `std::unique_ptr`

- It means **Exclusive Ownership**: only one owner.
- Only **one** unique_ptr can point to an object at a time.
- You cannot copy it (that is a compile error!). But you can **move** it.
- It is very light. It costs nothing extra compared to a raw pointer (zero overhead).

**Best Practice:** Create one with `std::make_unique<Type>(args)`.

```cpp
#include <iostream>
#include <memory> // Required

class Entity {
public:
    Entity() { std::cout << "Entity Created!" << std::endl; }
    ~Entity() { std::cout << "Entity Destroyed!" << std::endl; }
    void greet() { std::cout << "Hello from Entity" << std::endl; }
};

int main() {
    {
        // Create unique_ptr
        std::unique_ptr<Entity> entity = std::make_unique<Entity>();
        
        entity->greet();
        
        // std::unique_ptr<Entity> e2 = entity; // ERROR: Cannot copy!
        
    } // End of scope -> entity is destroyed automatically!
    
    std::cout << "Back in main" << std::endl;
    return 0;
}
```

### 5. `std::shared_ptr`

- It means **Shared Ownership**: many owners.
- Many shared_ptrs can point to the same object.
- It uses **Reference Counting**. It counts how many pointers to the object exist.
- The object is deleted only when the *last* shared_ptr is destroyed.

**Best Practice:** Use `std::make_shared<Type>(args)`.

```cpp
#include <iostream>
#include <memory>

class Resource {
public:
    ~Resource() { std::cout << "Resource freed" << std::endl; }
};

int main() {
    std::shared_ptr<Resource> ptr1;
    
    {
        std::shared_ptr<Resource> ptr2 = std::make_shared<Resource>();
        ptr1 = ptr2; // Sharing usage! Ref count = 2
        
        std::cout << "Ref count: " << ptr1.use_count() << std::endl;
        
    } // ptr2 goes out of scope. Ref count = 1. Resource NOT deleted.
    
    std::cout << "Ref count outside: " << ptr1.use_count() << std::endl;
    
    return 0;
} // ptr1 goes out of scope. Ref count = 0. Resource IS deleted.
```

### 6. The Problem of Circular Dependency

Say Object A has a shared_ptr to Object B. And Object B has a shared_ptr to Object A. Then their reference counts never go down to zero. So the objects are never deleted. This is a memory leak.

```cpp
#include <iostream>
#include <memory>

struct B;
struct A {
    std::shared_ptr<B> b_ptr;
    ~A() { std::cout << "A destroyed" << std::endl; }
};

struct B {
    std::shared_ptr<A> a_ptr;
    ~B() { std::cout << "B destroyed" << std::endl; }
};

int main() {
    auto a = std::make_shared<A>();
    auto b = std::make_shared<B>();
    
    a->b_ptr = b;
    b->a_ptr = a;
    
    std::cout << "End of main" << std::endl;
    return 0;
} // NEITHER DESTROYED! LEAK!
```

### 7. `std::weak_ptr`

A `std::weak_ptr` lets you watch a `shared_ptr` without adding to the reference count. This breaks the cycle.

You cannot use the object directly through a `weak_ptr`. First you must turn it into a `shared_ptr` with `.lock()`.

```cpp
#include <iostream>
#include <memory>

struct NodeB;
struct NodeA {
    std::shared_ptr<NodeB> b_ptr;
    ~NodeA() { std::cout << "NodeA destroyed" << std::endl; }
};

struct NodeB {
    std::weak_ptr<NodeA> a_ptr; // WEAK POINTER
    ~NodeB() { std::cout << "NodeB destroyed" << std::endl; }
};

int main() {
    auto a = std::make_shared<NodeA>();
    auto b = std::make_shared<NodeB>();
    
    a->b_ptr = b;
    b->a_ptr = a;
    
    std::cout << "End of main" << std::endl;
    return 0;
} // BOTH DESTROYED Cleanly!
```

### 8. Rule of Zero and Legacy Code

- **Rule of Zero**: if you use smart pointers, you usually do not need to write your own destructors.
- **Legacy Code**: old C-APIs need a raw pointer. Use `.get()` to get it. **NEVER** delete that pointer.

```cpp
#include <iostream>
#include <memory>

void legacyFunction(int* p) {
    std::cout << "Legacy Value: " << *p << std::endl;
}

int main() {
    std::unique_ptr<int> smart = std::make_unique<int>(999);
    
    legacyFunction(smart.get()); // OK: passes raw pointer
    
    return 0;
}
```

---

## New words

- **allocate**: reserve memory for your program.
- **release (free)**: give memory back.
- **memory leak**: memory that is never given back.
- **RAII**: get a resource in the constructor and give it back in the destructor.
- **ownership**: who is responsible for deleting an object.
- **reference counting**: counting how many pointers share one object.
- **circular dependency**: 2 objects that point to each other, so neither is deleted.
- **legacy code**: old code that you still have to work with.
