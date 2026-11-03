# Automate an Investigation: lesson

### 1. CSV files

CSV ("comma-separated values") is a table stored as text. The first line
is the header. It gives the names of the columns. Every other line is one
row. Look at observations.csv:

```
time,station,snr,status
1,ALPHA,10,LOCKED
2,BRAVO,50,SEARCHING
```

### 2. csv.DictReader

csv.DictReader reads each row as a dictionary. The keys are the column
names:

```
import csv
with open(input_path, newline="") as f:
    for row in csv.DictReader(f):
        print(row["station"], row["snr"])   # ALPHA 10
```

Every value arrives as a STRING. "10" is text. Before you do maths with
it, turn it into a number with float(row["snr"]).

### 3. Filter, then group

- Filter: skip the rows you do not want. Here, skip rows where the status
  is not LOCKED.
- Group: collect values that have the same key. Make one list per key:

```
groups = {}
for name, value in [("a", 1), ("b", 5), ("a", 3)]:
    if name not in groups:
        groups[name] = []
    groups[name].append(value)
# groups is {'a': [1, 3], 'b': [5]}
```

Then:

- len(groups["a"]) is how many values there are.
- sum(...) / len(...) is the average.
- round(2.345, 1) rounds to one decimal place: 2.3.

### 4. JSON

JSON is a text format for data. It looks like Python dicts and lists.
You can put dictionaries inside dictionaries (nested dictionaries):

```
import json
result = {"KIWI": {"count": 4, "average_snr": 7.5}}
with open(output_path, "w") as f:
    json.dump(result, f, sort_keys=True, indent=2)
```

sort_keys=True writes the keys in alphabetical order. So the same input
always gives exactly the same file. This is called "deterministic".
indent=2 only makes the file easier for people to read.

### 5. Derive everything from the input

`./check` runs your function on a DIFFERENT small CSV with different
stations. Do not type station names or numbers from observations.csv
into your code. If you do, the check fails. Let the code calculate
everything.

The `./run` script runs your program on observations.csv. Then it prints
report.json in a neat format. With a correct solution you see:

- ALPHA with count 3 and average_snr 15.0
- CHARLIE with count 3 and average_snr 9.0

BRAVO is missing, because its only row was not LOCKED.

## New words
- **CSV**: a text table. It has one row per line. Commas separate the columns.
- **header**: the first CSV line. It holds the column names.
- **csv.DictReader**: reads CSV rows as dictionaries. The keys are the column names.
- **filter**: keep only the items that pass a test.
- **group**: put items that have the same key together.
- **JSON**: a text format for nested data (dicts, lists, numbers, strings).
- **json.dump**: write a Python value to a file as JSON.
- **deterministic**: the same input always gives exactly the same output.
