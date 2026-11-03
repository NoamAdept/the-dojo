# Creating and Editing Text Files: lesson

### Reading a file with cat

You already met `cat`. It prints a file. It can also print several files, one after the other.
Its name comes from con**cat**enate. This word means "chain together".

```console
$ cat poem.txt
Night falls on the hill
...
$ cat poem.txt message.txt
```

### The vim editor

`echo` and `>` are fine for 1 line. But longer text needs a **text editor**. A text editor is a
program for writing and changing text. **vim** is an editor that you find on almost every
Linux machine. The Pi has it too.

Use this command to open a file. If the file does not exist, vim creates it.

```console
$ vim shopping.txt
```

The terminal turns into the editor. Lines that start with `~` are past the end of the file.

vim has **modes**. A mode is the job vim is doing right now. This is the 1 big idea to learn:

- **Normal mode** is where vim starts. Here, keys are *commands*, not text.
  For example, if you press `x`, vim deletes a character. It does not type an x.
- **Insert mode** is for typing. Press **`i`** to enter it. The bottom line shows `-- INSERT --`.
  Now you can type normally. Use Enter for new lines. Use Backspace to delete.
- Press **`Esc`** to go back to Normal mode. If you are not sure which mode you are in, press Esc.

Commands for saving and quitting start with `:`. Type them in Normal mode.
They appear at the bottom of the screen.

| Type | Does |
|------|------|
| `:w` then Enter | save ("write") |
| `:q` then Enter | quit (only works if there is nothing unsaved) |
| `:wq` then Enter | save and quit |
| `:q!` then Enter | quit and **throw away** your changes |

So the usual steps are:

1. `vim FILE`
2. **`i`**
3. Type your text.
4. **`Esc`**
5. **`:wq`** and Enter.

Back at the prompt, check the result with `cat FILE`.

Some Normal mode keys help you fix text. The **cursor** is the blinking mark that shows your place.

- The arrow keys move the cursor. The keys `h` `j` `k` `l` also move it.
- `x` deletes the character under the cursor.
- `a` starts Insert mode just *after* the cursor. This is useful for adding a letter.
- `dd` deletes the whole line.
- `u` undoes the last change.

Maybe you get lost. For example, strange text appears at the bottom, or keys do odd things.
Then do this:

1. Press **Esc** 2 times.
2. Type **`:q!`** and press Enter.

You are back at the prompt. The file has not changed, so you can start again.

(If the shell cannot find `vim`, try `vi`. It is a smaller version that is always installed.)

### New words

- **text file**: a file that holds plain letters and lines. People can read it.
- **text editor**: a program for writing and changing text files.
- **vim**: the standard terminal text editor on Linux.
- **mode**: vim's current job. Normal mode runs commands. Insert mode types text.
- **cursor**: the blinking mark that shows where your typing goes.
- **`i`, `Esc`, `:wq`, `:q!`**: start typing, stop typing, save and quit, quit without saving.
- **`cat`**: prints 1 or more files.

## Offline help

- Run `vimtutor` in your terminal. It is a 30 minute hands-on lesson that comes with vim.
- The vim help: inside vim, type `:help` and Enter. `:q` closes it. Offline: `man vim`, `man cat`.
