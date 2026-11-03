# Your First Commands: lesson

### The terminal and the shell

A **terminal** is a window where you talk to the computer. You type words instead of clicking.
A program called the **shell** runs inside the terminal. The shell works like this:

1. It waits for you to type a line.
2. You press **Enter**, and it runs the line.
3. It shows you the result.
4. It waits again.

The shell we use is called **bash**.

When the shell is ready for you, it shows a **prompt**. A prompt is a short piece of text.
It usually ends in `$`. Here is an example:

```console
hacker@pi:~/challenge$
```

You type after the `$`. In this course, examples look like this:

```console
$ echo hello
hello
```

The first line starts with `$`. That line is what you type.
**Do not type the `$` itself.** It only stands for the prompt.
The line below it is what the computer prints back. We call this the **output**.

(On a Mac, the prompt may end in `%` instead of `$`. That is a different shell, called zsh.
Type `bash` and press Enter to switch to bash. Then everything here works the same.)

### Commands and arguments

A **command** is the name of a program that you want to run. Try these commands one at a time.
Press Enter after each one:

```console
$ whoami
hacker
$ date
Tue Oct  6 14:03:12 UTC 2026
```

`whoami` prints your user name. Your name will be different from `hacker`.
`date` prints the date and the time.

You can type more words after the command. These words are **arguments**. An argument is extra
information for the command. The shell splits your line at each space:

- The first word is the command.
- The other words are arguments.

```console
$ echo Hello terminal
Hello terminal
```

Here `echo` is the command. `Hello` and `terminal` are 2 arguments. `echo` just prints its
arguments back to you. Capital letters matter: `echo` works, but `Echo` does not.

### Saving output into a file

Output normally goes to the screen. The `>` sign sends it into a file instead.
If the file does not exist, the shell creates it.
If the file already exists, the shell **replaces** it.

```console
$ echo Hello terminal > hello.txt
$
```

This time nothing is printed. The text went into `hello.txt` instead.

- To see the files in this folder, type `ls`. The name is short for "list".
- To print what is inside a file, type `cat` and then the file name.

You will learn more about both commands soon.

```console
$ ls
README.md  check  check.py  hello.txt
$ cat hello.txt
Hello terminal
```

Two arrows, `>>`, **add** to the end of a file. They do not replace it.

```console
$ echo apples > fruit.txt
$ echo pears >> fruit.txt
$ cat fruit.txt
apples
pears
```

Did you make a mistake? Just run the command again. `>` writes over the file with the new output.

### Checking your work

Every challenge has a program called `check`. Type `./check` and press Enter. It tells you 2 things:

- how many tasks pass
- what is still wrong

A later challenge explains what the `./` means. For now, just type it like that.

### New words

- **terminal**: the window you type commands into.
- **shell**: the program inside the terminal. It reads and runs your commands. Ours is bash.
- **prompt**: the text that ends in `$`. It means "I am ready. Type something."
- **command**: the name of a program to run, like `date`.
- **argument**: an extra word after the command, like `hello` in `echo hello`.
- **output**: what a command prints.
- **`>` and `>>`**: send output into a file. `>` replaces the file. `>>` adds to the end of it.

## Offline help

- Offline manual pages: type `man echo` or `man date` in your terminal. Press `q` to leave.
