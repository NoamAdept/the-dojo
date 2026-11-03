# Classes: Private Data and Constructors: lesson

### Another way to write a constructor

In the C++ Qualification you will often see a shorter form. It is called a **member initializer list**. It does the same thing as the constructor in `README.md`:

```cpp
Counter(int start) : count(start) {}
```

In this challenge you can use either form.

### Why do this? To protect the rules

Imagine a radio that only tunes from 88 to 108 MHz. Make the frequency private. Then the only way to change it is a method. And the method can refuse bad values:

```cpp
void tune(double newMhz) {
    if (newMhz >= 88.0 && newMhz <= 108.0) {
        mhz = newMhz;
    }
    // anything else is ignored, so mhz is always valid
}
```

### New words

- **class**: like a struct, but its members are private. Only members under `public:` are public.
- **public**: anyone can use this member.
- **private**: only the methods of the class itself can use this member.
- **constructor**: a method with the same name as the class and no return type. It runs when an object is made.
- **getter**: a small method that returns a private field.
- **member initializer list**: a short way to set fields in a constructor: `Counter(int start) : count(start) {}`.
