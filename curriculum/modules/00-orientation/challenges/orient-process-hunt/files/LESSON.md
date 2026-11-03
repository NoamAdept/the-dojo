# Process Hunt: lesson

A program is a file on disk. When you start it, the computer loads it and
runs it. That running copy is called a process. Every process gets a
number. This number is its process ID, or PID. The system uses the PID to
tell processes apart.

A process can run "in the background". This means it keeps working, but
your prompt comes back at once. It also prints nothing. `./run` starts one
helper like this. It does not tell you the PID. That is on purpose.

ps lists processes. ps aux lists all of them, with details:

```
$ ps aux | grep sleep
student   4242  0.0  0.0   5480  1000 pts/0  S  10:00  0:00 sleep 300
student   4250  0.0  0.0   6400  2100 pts/0  S+ 10:00  0:00 grep sleep

column 1   the user who owns the process
column 2   the PID (here 4242)
last part  the command that started it
```

The second line is your own grep, which looks for "sleep". Ignore it.
pgrep prints only the PID. This is useful:

```
$ pgrep -f 'sleep 300'
4242
```

Linux shows every process as a folder under /proc. The folder name is the
PID. Two useful things are in that folder. (Replace 4242 with your PID.)

```
/proc/4242/cmdline   the full command that started it, including the
                     arguments (the extra words after the program name)
/proc/4242/cwd       a link to the folder the process is working in
```

In cmdline, the words are not separated by spaces. They are separated by
an invisible "zero" character. So cat prints them all stuck together. tr
can change each zero into a space. The ; echo part only adds a newline at
the end:

```
$ tr '\0' ' ' < /proc/4242/cmdline ; echo
sleep 300

$ readlink /proc/4242/cwd
/home/student/somewhere
```

readlink prints where a link points. A Mac has no /proc. On a Mac, use
these commands instead:

- ps -p PID -o command=
- lsof -a -p PID -d cwd -Fn

Arguments often look like --name value. Here is an example:

```
mytool --config /tmp/x/settings.txt
```

The path after --config is a file. You can open it with cat.

report.txt is a list of key=value lines. Open it in a text editor. For
example, run vim report.txt. Then:

1. Press i.
2. Type each answer after its = sign.
3. Press Esc.
4. Type :wq and press Enter. This saves the file and quits.

Lines that start with # are comments for humans. The checker ignores them.

## New words
- **process**: a program that is running now.
- **PID**: the number that identifies one process.
- **background**: running without holding your prompt.
- **argument**: an extra word given to a command when it starts.
- **/proc**: a pretend folder where Linux shows live facts about processes.
- **cmdline**: the file in /proc/PID that holds the start command.
- **cwd**: current working directory, the folder a process is "standing" in.
- **comment**: a line for humans that the program ignores.

## Offline help

- man ps
- man 5 proc     (offline: everything in /proc; search with /cmdline)
