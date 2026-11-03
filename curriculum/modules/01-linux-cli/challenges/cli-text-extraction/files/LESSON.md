# Text Extraction: lesson

Plain grep finds a fixed word. But often you want to find text with a
certain shape. For example: "anything that looks like a price", or
"anything that looks like a time". A regular expression (regex) is a
small pattern language. It describes shapes of text.

These are the pieces you need:

```
[0-9]     any one digit
+         the thing before me, one or more times
[0-9]+    one or more digits, such as 7, 42 or 2026
\.        a real dot (a bare . means "any character")
' '       a space matches a space
```

So `[0-9]+\.[0-9]+` means: digits, then a dot, then digits. It matches
3.14 and 12.50. It does not match 12, because there is no dot. It does
not match 3. either, because there are no digits after the dot.

grep options:

```
-E   use "extended" regex, so + works without extra backslashes
-o   print only the matching part, each match on its own line
```

Here is an example file, prices.txt:

```
Tea 2.50 EUR, cake 3.10 EUR, table 4.
Coffee 2.50 EUR again.

$ grep -oE '[0-9]+\.[0-9]+ EUR' prices.txt
2.50 EUR
3.10 EUR
2.50 EUR
```

Look at the result. grep skipped "4.". It also skipped words that do not
have EUR after them. Put the pattern in single quotes. Then the shell
does not change any of its characters.

To remove the unit, cut the line at the space and keep field 1:

```
cut -d' ' -f1
```

sort -n sorts as numbers. If you add -u (unique), sort also removes
repeated lines:

```
$ grep -oE '[0-9]+\.[0-9]+ EUR' prices.txt | cut -d' ' -f1 | sort -n -u
2.50
3.10
```

Then use > to save the result in a file.

## New words
- **regular expression (regex)**: a pattern that describes a shape of text.
- **`[0-9]`**: one character from the range 0 to 9.
- **`+`**: "one or more of the previous thing".
- **`\.`**: a literal dot (a real dot character).
- **grep -o**: print only the matched text.
- **grep -E**: use extended regex syntax.
- **sort -u**: sort and drop duplicate (repeated) lines.
- **MHz**: megahertz, a unit of radio frequency (millions of cycles per second).

## Offline help

- man grep
- man 7 regex    (offline: regex syntax)
