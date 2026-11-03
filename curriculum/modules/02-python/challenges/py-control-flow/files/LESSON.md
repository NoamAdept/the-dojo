# Classify Signal Strengths: lesson

### 1. Functions return, they do not print

`./check` does not read what your program prints. It imports classify.py
(loads the file so it can use its functions). Then it calls your functions
directly, like this:

```
classify_signal(5)        # ./check expects the string "usable"
```

So each function must use `return`, not `print`. Some functions reach the
end without a `return` (like the starter's `pass`). These functions give back
a special value called None. This is why the starter prints None.

### 2. One chain, one answer

An if/elif/else chain is a list of tests. Python tests the conditions from
top to bottom. It runs only the FIRST branch that is true:

```
def size_word(n):
    if n < 10:
        return "small"
    elif n < 100:      # we only get here if n >= 10
        return "medium"
    else:
        return "large"
```

The order matters. Because of the order, the second test only needs to
check the upper edge.

### 3. Boundaries are where bugs hide

A "boundary" is the exact value where the answer changes. Here the
boundaries are:

- 4 and 5
- 14 and 15

Read the rules below carefully. Is 5 weak or usable? Is 15 usable or
strong? `./check` tests exactly those values. It also tests negative
numbers and big numbers.

### 4. Counting with a dictionary

A dictionary stores pairs of a key and a value. To count, start every
label at zero. Then add one each time you see that label:

```
counts = {"red": 0, "blue": 0}
for colour in ["red", "red", "blue"]:
    counts[colour] = counts[colour] + 1
# counts is now {'red': 2, 'blue': 1}
```

Starting at zero is important. A label that never appears must still be
in the dictionary, with the value 0.

### 5. The provided main block (you do not need to change it)

`sys.argv` is a list of the words you type after `python3` on the command
line. For `python3 classify.py 2 8 19` it is
['classify.py', '2', '8', '19'].

- `sys.argv[1:]` removes the file name from the list.
- `[int(x) for x in sys.argv[1:]]` builds a new list. It turns each word
  into a whole number. This short form is called a "list comprehension".

The line `if __name__ == "__main__":` means "only run this part when you
start the file directly". So this part does not run when `./check`
imports the file.

When everything works, the try command prints something like this:

```
{'weak': 1, 'usable': 1, 'strong': 1}
```

## New words
- **return**: gives a value back to the code that called the function.
- **None**: Python's "no value here" value. A function gives None when it has no return.
- **elif**: "else if". Another test. Python tries it only when the tests above were false.
- **boundary**: the exact input where the right answer changes.
- **sys.argv**: a list of the words typed on the command line.
- **list comprehension**: [something(x) for x in a_list]. It builds a new list.
- **import**: load another Python file so you can use its functions.
- **dictionary**: a collection of key and value pairs, like {"red": 0}.
