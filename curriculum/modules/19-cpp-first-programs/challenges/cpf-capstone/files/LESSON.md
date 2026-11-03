# Capstone: A Signal Level Report: lesson

### The tool

A radio receiver measures the strength of a signal in dBm. These are usually negative numbers. -40 is a strong signal. -90 is a weak signal. Your program takes levels as arguments. Then it prints a report:

```
$ ./report -40 -72 -55
readings: 3
smallest: -72
largest: -40
average: -55.67
strong: 2
```

"strong" counts the readings that are -60 or higher.

### One pass over the words

You do not need to keep all the levels. Go over the words one time with a for loop (like in `./add`). As you go, update a few running values:

- a running total (the accumulator pattern), for the average;
- the smallest level so far, and the largest level so far;
- how many strong levels you saw.

How to find the "smallest so far":

1. Start with the **first** level.
2. For each next level, keep the smaller of the two.

`report.cpp` already has the function `larger(a, b)`. It is an example of a helper function. You can use it for the "largest so far". You write `smaller(a, b)`.

```cpp
int first = std::stoi(argv[1]);
int low = first;
int high = first;
// then, inside the loop, for each level:
//     high = larger(high, level);
```

### Check the input first

A careful program **checks its input before it uses it**. This is called **validation**.

- With no levels, there is nothing to report. So print a usage line and return 1.
- If a word is not a number, say which word. Then return 1. Use try/catch around std::stoi, like in the last challenge.

### No new syntax

You already did everything here in earlier challenges. If you do not know what to do, look back at them.

### New words

- validation: checking that the input is OK before you use it.
- running value: a variable that changes on each pass of a loop. For example, a total or the smallest value so far.
- dBm: a unit for the power of a radio signal. A value closer to 0 is stronger.
