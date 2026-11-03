# Comprehending Commands: lesson

### How these shell challenges work

Each task is a very small bash script. Write your command(s) in `answers/taskN.sh`. Replace the
`TODO` line with them.

`./check` runs every script in a new copy of a small fake filesystem. It throws the copy away
afterwards. Then it looks at what happened:

- what the script printed,
- which files exist,
- how the challenge programs were started.

Some rules:

- The root folder of the fake filesystem is in the variable `$DOJO`. The original pwn.college level
  may talk about `/challenge/run`. Then you write `"$DOJO/challenge/run"` (keep the double quotes).
- During the check, `$HOME` (and `~`) is `$DOJO/home/hacker`. Every script starts in that folder.
- The check uses its own secrets and file names. They are different from the practice copy. So your
  script must print or copy what the task asks for. If you paste an answer that you saw 1 time, it
  will not work.

To explore, use the practice copy in `dojo/`. First, run `. ./env.sh` 1 time in your terminal. It
sets `DOJO`, and it adds the fake `bin/` folder to your `PATH` (the list of folders where the shell
looks for commands). Then look around, for example with `ls "$DOJO"`.

`./try N` runs `answers/taskN.sh` in the same way as the check, but inside the practice copy. It may
change files in `dojo/`. This never changes the result of `./check`.
