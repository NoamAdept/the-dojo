# Getting Help and Handy Keys: lesson

### Options and --help

Many commands accept **options**. An option is a special argument that starts with `-` or `--`.
It changes what the command does. For example:

- `ls -l` lists files with details.
- `wc -l` counts lines.

Almost every command explains its options when you give it `--help`:

```console
$ wc --help
Usage: wc [OPTION]... [FILE]...
Print newline, word, and byte counts for each FILE...
  -c, --bytes            print the byte counts
  -l, --lines            print the newline counts
...
```

Read it like a menu. Each line shows an option and what it does. `[FILE]...` means "you may
give 1 or more file names".

Is the help longer than your window? Then scroll up with the mouse wheel, or press
Shift+PageUp. (The `man` command shows full manuals. You will use it in Linux Shell Basics.)

`date` has a special kind of argument: a **format**. A format starts with `+`. `date --help`
lists the pieces you can use in it. For example, `%H` is the hour:

```console
$ date +%H
14
```

### Tab completion

Type the start of a file name or command name. Then press **Tab**.

- If only 1 name fits, bash fills in the rest.
- If several names fit, press Tab 2 times to see them all.

This saves typing and stops typing mistakes. Try it: first run `. ./env.sh`. Then type
`cat "$DOJO/signals/a` and press Tab.

### History: the up arrow

Bash remembers your commands. We call this list the **history**.

1. Press the **up arrow** to bring back the last command. Press it again for older ones.
2. If you want, change the command. Use the left and right arrows to move.
3. Press Enter to run it.

The `history` command lists what you typed.

### Stopping a program: Ctrl-C

Some programs run until you stop them. Sometimes a command just seems stuck. To stop
("interrupt") the running program, hold **Ctrl** and press **C**. You get your prompt back.

Note: Ctrl-C does not copy text in the terminal. To copy, select the text with the mouse.
Then use the terminal's menu. Many Linux terminals also use Ctrl+Shift+C to copy.

2 more handy keys: **Ctrl-L** clears the screen. The `clear` command does the same.

The answers in this challenge work like the last challenge:

- Your scripts go in `answers/`.
- The practice copy is in `dojo/`.
- `. ./env.sh` sets `DOJO`.
- `./try N` tests task N.

### New words

- **option**: an argument that starts with `-` or `--`. It changes what a command does, like `-l`.
- **`--help`**: the option that makes a command describe itself.
- **Tab completion**: press Tab to let bash finish a name for you.
- **history**: the list of commands you typed. The up arrow walks back through it.
- **Ctrl-C**: stop the program that is running now.

## Offline help

- Offline: `wc --help`, `date --help`, `help history`.
