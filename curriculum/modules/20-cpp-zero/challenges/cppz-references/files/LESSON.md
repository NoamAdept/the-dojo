# References: Another Name for a Variable: lesson

### Functions get copies

When you call a function, each parameter gets a **copy** of the value you passed. This is called **pass by value**. The function can change its copy. But your variable stays the same:

```cpp
void addOneToCopy(int x) {
    x = x + 1;        // changes the copy only
}

int n = 4;
addOneToCopy(n);      // n is still 4
```

Usually this is what you want. A function cannot break your variables by accident. To get a result out of a function, you `return` it. But sometimes you do want a function to change your variable. For example:

- to swap two variables
- to change every item of a list

For this, C++ has references.

### A reference: a second name

A **reference** is another name for a variable that already exists. To make one, write `&` after the type:

```cpp
int n = 4;
int& other = n;   // "other" is now a second name for n
other = 10;       // n is 10 too: it is the same variable
```

You can use a reference as a function parameter. It means "use the caller's variable itself, not a copy". (The caller is the code that calls the function.)

```cpp
void addOne(int& x) {
    x = x + 1;        // changes the caller's variable
}

int n = 4;
addOne(n);            // n is now 5
```

The only difference from `addOneToCopy` is the `&` in `int& x`. The call looks the same. There are 2 rules:

- You must tie a reference to a variable when you make it.
- A reference always stays tied to that same variable.

### Changing every item in a vector

`for (int x : v)` gives you a copy of each item. So if you change `x`, nothing changes in `v`. Add `&` to get the item itself:

```cpp
for (int& x : v) {
    x = 0;            // sets every item of v to 0
}
```

### const reference: look but do not touch

When you pass a vector **by value**, every item is copied. This is slow for a big list. When you pass by reference, there is no copy. But then the function could change your list by mistake. `const` fixes that:

```cpp
int countItems(const std::vector<int>& v) {   // no copy, and v cannot be changed here
    return v.size();
}
```

Some functions only read a string or a vector. From now on in this course, these functions take them as `const std::string&` and `const std::vector<...>&`.

### New words

- **pass by value**: the function gets its own copy of each argument (`void f(int x)`).
- **reference**: another name for an existing variable, written `int& r = n;`.
- **pass by reference**: the function works on the caller's variable, not a copy (`void f(int& x)`).
- **const**: "this cannot be changed here".
- **const reference**: `const std::vector<int>& v`. There is no copy and no changes. This is the usual way to pass big values that you only read.
- **int& in a for loop**: `for (int& x : v)` visits the real items, so you can change them.
