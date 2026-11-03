# Practicing Piping

Every program starts with 3 open channels (streams of data):

- **stdin** (number 0): input.
- **stdout** (number 1): normal output.
- **stderr** (number 2): error messages and other extra messages.

The shell can connect these channels to other places:

| syntax | meaning |
|---|---|
| `cmd > file` | stdout into file (truncates it first: the old contents are deleted) |
| `cmd >> file` | stdout appended to the end of file |
| `cmd 2> file` | stderr into file |
| `cmd < file` | file becomes stdin |
| `cmd 2>&1` | send stderr wherever stdout currently goes |
| `a \| b` | a's stdout becomes b's stdin (a **pipe**) |

```console
$ echo hi > greeting; cat greeting
hi
$ ls /nope 2> errors.log
$ grep -v DEBUG < app.log | grep ERROR
```

Some filters are very useful in pipes:

- `grep -v WORD` keeps the lines that do NOT contain WORD.
- `sed 's/old/new/g'` replaces every `old` with `new`. (`s/old//g` deletes it.)

**tee FILE** copies its stdin to 2 places: to FILE and to stdout.
So `a | tee copy.txt | b` lets you see the data that goes from a to b.

**Process substitution** turns a command into a file name:

- `<(cmd)` is a file. When you read it, you get the output of cmd.
- `>(cmd)` is a file. What you write to it goes to the stdin of cmd.

Some examples:

- `diff <(cmd1) <(cmd2)` compares 2 outputs.
- `cmd | tee >(a) | b` sends the output to both a and b.
- `cmd 2> >(a) | b` sends stderr to a and stdout to b.

**Named pipes** (FIFOs, "first in, first out") are pipes with a name in the filesystem.
You make one with `mkfifo NAME`.
A program that writes to a FIFO blocks (waits) until another program reads from it.
So, in 1 script:

1. Start one side in the background with `&`.
2. Run the other side.
3. Then run `wait`.

New to this? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

All programs are in `$DOJO/challenge/`. Your script starts in your home directory. So files with a plain name, like `myflag`, are created there.

1. **Redirecting output**: write the word `PWN` into a file named `COLLEGE`. Use `echo` and `>`.
2. **Redirecting more output**: run `run`, and redirect its stdout to the file `myflag`.
3. **Appending output**: run `append`, and append (`>>`) its stdout to the end of `~/the-flag`. (`append` writes the first half of the file itself. If you truncate the file, you delete that half.)
4. **Redirecting errors**: run `run`. Send its stdout to `myflag` and its stderr to `instructions`.
5. **Redirecting input**: create a file `PWN` that contains `COLLEGE`. Then run `needinput`, and redirect that file into its stdin.
6. **Grepping stored results**: redirect the output of `noisy` to `$DOJO/tmp/data.txt`. Then print only the line of that file that contains `academy{`.
7. **Grepping live output**: pipe `noisy` into `grep`. Print only the line that contains `academy{`.
8. **Grepping errors**: `noisyerr` prints the same large amount of lines, but on stderr. Print only the line that contains `academy{`.
9. **Filtering with grep -v**: `decoys` prints many lines that contain `DECOY`, and 1 real secret. Print only the real one.
10. **Filtering with sed**: `fakeflag` prints a secret with `FAKEFLAG` between each pair of characters. Print it with every `FAKEFLAG` removed.
11. **Duplicating piped data with tee**: pipe `pwn` into `college`. Put `tee ~/pwn.log` in the middle, so a copy is saved. But first, `pwn` needs an argument. Run it 1 time on its own (or read the log) to see what it asks for.
12. **Process substitution for input**: use `diff` with `<(...)` to compare the outputs of `print_decoys` and `print_decoys_and_flag`. Only the extra line must show.
13. **Writing to multiple programs**: send the stdout of `hack` to both `the` and `planet`.
14. **Split-piping**: send the stderr of `hack` to `the` and its stdout to `planet`.
15. **Named pipes**: create the FIFO `$DOJO/tmp/flag_fifo`. Redirect the stdout of `fifo` into it. Then print what comes out of the FIFO (for example with `cat`). Do both sides in your 1 script.

## Check your work

You can run `./check` as many times as you want. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
