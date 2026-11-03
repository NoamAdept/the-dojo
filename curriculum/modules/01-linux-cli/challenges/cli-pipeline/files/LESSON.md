# Pipeline Practice: lesson

CSV means "comma separated values". A CSV file is a table stored as text.
Each line is a row. Commas split the row into columns. Columns are also
called fields. The first line is often a header. The header gives the
names of the columns:

```
name,colour,score
ann,red,7
bob,blue,12
cat,red,30
```

A pipe | sends the output of one command into the next command. Each
command does 1 small job. Build the chain 1 step at a time. Look at the
output after each step.

### grep: keep matching lines

`grep TEXT` keeps only the lines that contain TEXT:

```
$ grep ',red,' scores.csv
ann,red,7
cat,red,30
```

The commas in the pattern are important. They make sure you match the
whole column value. Without them, you could also match a name that
contains "red" by chance.

### sort: put lines in order

Useful options:

```
-t,      fields are split by commas
-k2,2    sort by field 2 only (start field 2, end field 2)
n        compare as numbers, so 30 comes after 7
r        reverse: biggest first
```

```
$ grep ',red,' scores.csv | sort -t, -k3,3nr
cat,red,30
ann,red,7
```

Without n, sort compares text, not numbers. Then "7" comes after "30",
because the character 7 is bigger than the character 3.

### head and cut: keep the part you need

```
head -n 2        keep only the first 2 lines
cut -d, -f1      split on commas (-d = delimiter) and keep field 1
```

```
$ grep ',red,' scores.csv | sort -t, -k3,3nr | head -n 1 | cut -d, -f1
cat
```

### Save it

At the end, > FILE sends the output into a file, not to the screen. It
replaces everything that was in the file before:

```
$ echo hello > greeting.txt
$ cat greeting.txt
hello
```

## New words
- **CSV**: a table as text, one row per line, commas between columns.
- **field / column**: one value in a row.
- **header**: the first line, which names the columns.
- **pipe (|)**: sends one command's output into the next command.
- **delimiter**: the character that separates fields, here a comma.
- **numeric sort**: comparing as numbers, not as text.
- **redirect (>)**: saves output into a file.

## Offline help

- man sort
- man cut
