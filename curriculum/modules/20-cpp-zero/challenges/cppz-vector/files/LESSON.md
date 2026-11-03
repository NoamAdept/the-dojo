# Lists with std::vector: lesson

### Range-based for

You can loop with an index, the same way as over a string. Write `for (std::size_t i = 0; i < v.size(); i++)` and then use `v[i]`. C++ also has a shorter loop. It visits every item in order:

```cpp
for (int x : v) {
    std::cout << x << std::endl;
}
```

Read it as "for each `x` in `v`". `x` is a copy of one item. Each time round the loop, `x` is the next item. This loop works on strings too: `for (char c : text)`.

### Returning a vector

A function can build a vector. Then it can return the whole list:

```cpp
std::vector<int> firstSquares(int n) {
    std::vector<int> out;          // starts empty
    for (int i = 1; i <= n; i++) {
        out.push_back(i * i);
    }
    return out;                    // firstSquares(3) is {1, 4, 9}
}
```

In this challenge the functions take their vector **by value**. This means each function gets its own copy. That is fine for now. The next challenge shows how to avoid the copy.

### New words

- **std::vector**: a list of values of one type that can grow.
- **<int> (angle brackets)**: tells what type the vector holds.
- **push_back**: adds one item at the end of a vector.
- **empty()**: `true` when the vector has no items.
- **range-based for**: `for (int x : v)` visits every item of `v` in order.
- **by value**: the function gets its own copy of the argument.
