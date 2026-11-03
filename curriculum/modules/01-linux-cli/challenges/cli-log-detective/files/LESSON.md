# Log Detective: lesson

A log is a text file. A program writes 1 line in it for each event
(each thing that happens). This log is "structured". This means:

- every line has the same parts, in the same order,
- a single space separates the parts,
- most parts are key=value pairs.

```
2026-01-01T09:00:00Z level=INFO component=fan message=spinning
|____ field 1 _____| |_field 2_| |_ field 3 _| |__ field 4 __|
```

level says how serious the event is (INFO, WARN, ERROR). component says
which part of the program wrote the line.

Here are the tools, step by step. Try each one alone first:

```
grep ' level=WARN ' FILE
    Keeps WARN lines. The spaces around the text make sure you match
    the whole field, so a value like level=WARNING would not sneak in.

cut -d' ' -f3
    Splits each line at spaces and keeps field 3.
    cut -d= -f2 then splits "component=fan" at = and keeps "fan".

sort | uniq -c
    uniq -c counts runs of identical lines that sit next to each other,
    so always sort first to bring equal lines together:

    $ printf 'cat\ndog\ncat\n' | sort | uniq -c
          2 cat
          1 dog

    The count comes first, then the word. sort also puts them in
    alphabetical order, which is what the report needs.

awk '{print $2 "=" $1}'
    awk splits each line into words; $1 is the first word, $2 the
    second. This prints them swapped, joined by an = sign:

    $ echo '5 apples' | awk '{print $2 "=" $1}'
    apples=5
```

Join the pieces with pipes (|). Look at the output after every step.
When the output looks right, add > report.txt at the end. This saves the
output in the file.

## New words
- **log**: a text file where a program writes what happens.
- **event**: one thing that happens, written as 1 line in the log.
- **structured log**: a log where every line follows the same layout.
- **key=value**: a name and its value joined by an equals sign.
- **field**: one part of a line.
- **level**: how serious a log event is (INFO, WARN, ERROR).
- **component**: the part of the program that wrote the line.
- **uniq -c**: counts identical lines that are next to each other.
- **awk**: a small tool that splits lines into words ($1, $2, ...) and prints them.

## Offline help

- man uniq
- man awk
