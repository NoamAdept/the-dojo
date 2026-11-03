# Lookups with std::map and auto: lesson

### Careful with [ ]

What if you use `ages["zoe"]` and the key is not in the map? Then `[ ]` **adds** the key, with value 0. This is useful for counting:

```cpp
std::map<std::string, int> seen;
seen["fm"]++;      // "fm" was missing, so it starts at 0 and becomes 1
seen["fm"]++;      // now 2
```

But it is a surprise when you only want to look. To look without adding a key:

- `ages.count("zoe")` is 1 if the key is there. It is 0 if the key is not there.
- `ages.at("ada")` gives the value. If the key is missing, it stops the program with an error.

Some maps are `const`, for example a `const std::map<...>&` parameter. On a `const` map, `[ ]` does not compile, because it might add a key. Use `count` and `at` on a `const` map.

### Looping over a map, and auto

A map keeps its keys **sorted**. For strings, this means alphabetical order. Each item is a **pair** (2 values together):

- `.first` is the key.
- `.second` is the value.

```cpp
for (const auto& entry : ages) {
    std::cout << entry.first << " is " << entry.second << std::endl;
}
// ada is 36
// bob is 41
```

`auto` means "compiler, find the type for me". The real type of `entry` is `std::pair<const std::string, int>`. That is long to type. More examples:

- `auto x = 5;` makes an `int`.
- `auto s = std::string("hi");` makes a `std::string`.

The `const ... &` is the const reference from the References challenge. It means no copy and no changes.

In C++17 you can also give the 2 parts their own names: `for (const auto& [name, age] : ages)`. You can use either style.

Sometimes you need to join a number to text. First turn the number into text with `std::to_string(36)`. This gives `"36"`.

### New words

- **std::map**: a sorted collection of key-to-value pairs. Each key is in it only once.
- **key / value**: what you look up / what you get back.
- **count(key)**: 1 if the key is in the map, and 0 if it is not.
- **at(key)**: the value for a key that must exist.
- **pair, .first, .second**: one map item (pair), its key (.first) and its value (.second).
- **auto**: lets the compiler pick the type from the value.
- **std::to_string**: turns a number into a `std::string`.
