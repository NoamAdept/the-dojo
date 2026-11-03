# Signal Dojo

An offline lab that teaches programming from zero: **4 belts, 110 challenges, Linux → C++ → Python**. It runs on a Raspberry Pi, any Linux or macOS machine, or Windows through WSL (anything with `python3`).

## Run it

```bash
tar -xzf pi-sdr-academy.tar.gz && cd pi-sdr-academy
./run.sh            # open the URL it prints; each learner creates an account, progress autosaves
```

Press **Read lesson** to learn the idea, **Start** to get the files, solve, run `./check`, then press **Done**.
Each learner's files are in their own folder, `~/signal-dojo/<username>` (a link to
`.academy-data/classroom/users/<username>/challenge`); on the machine running `./run.sh` a terminal opens there.

**Windows laptops and desktops:** run it inside WSL (Ubuntu 24.04), still from the one tarball and with no
internet on the laptop. See [docs/WSL.md](docs/WSL.md): a prepared image installs with one PowerShell command.

One-page guide for learners and admins: [docs/signal-dojo-guide.pdf](docs/signal-dojo-guide.pdf) (rebuild with `./scripts/build_guide.sh`).

### Save your work

**Save to a file** (in the lab, under Progress) downloads one `.zip` with your progress and every script you
wrote. **Restore** on any copy of Signal Dojo, even on another machine, brings it back; it only adds, so
nothing already solved is lost. From a terminal: `./academy save` (writes `~/signal-dojo/signal-dojo-save-DATE.zip`)
and `./academy restore FILE`.

Start empties the challenge folder, so the files you wrote or changed are kept first (in `.academy-data/work/`)
and come back when you start that challenge again. **Restart** on the challenge you are in gives you clean
starter files. Files over 5 MB (large data files) are not kept; they come back with the challenge.

No pip, no internet. To build the tarball: `./scripts/pack_portable.sh` (→ `dist/`).

## Belts

| Belt | What you learn |
|------|----------------|
| White | Terminal from zero, shell basics |
| Yellow | Processes, users, permissions, scripts, services |
| Orange | C++ from zero: first programs, strings, vectors, classes, files, then pointers and bytes, gdb, Linux system calls and the C++ qualification |
| Blue | Python from zero to qualification |

Each challenge folder has a short `README` (the tasks) and a `LESSON` (the teaching, new words, further reading). Both open inside the app too.

## Lab machine packages

```bash
sudo apt install vim tmux curl less man-db manpages manpages-dev build-essential gdb cmake pkg-config \
                 git tree net-tools netcat-openbsd iproute2 lsof procps psmisc
sudo update-alternatives --set editor /usr/bin/vim.basic   # make vim the system editor
```

The course teaches **vim** as the one text editor. `./run.sh` and the terminal the app opens
set `EDITOR`/`VISUAL` to vim (or `vi` if vim is missing), so `git commit`, `crontab -e` and
`sudoedit` open vim too. The `update-alternatives` line above does the same for any shell.

## Admin mode: open any challenge

```bash
ACADEMY_ADMIN=1 ./run.sh
```

Every belt is unlocked. Open `http://127.0.0.1:8080/`, enter the lab, and use the **Admin mode** box to jump to
any challenge by id or title, then press **Start**. `http://127.0.0.1:8080/admin` lists every challenge with a
filter, and a link like `http://127.0.0.1:8080/#challenge/pyq-generics` opens one directly. From a
terminal, `ACADEMY_ADMIN=1 ./academy start pyq-generics` stages it in `~/signal-dojo/challenge` (the
no-login folder; `ACADEMY_USER=<username>` in front uses that learner's folder instead).
Admin mode is ignored by the classroom server (`./academy serve`), so learners never get it.

### Turn dojos and challenges on or off

`/admin` has a **Turn dojos and challenges on or off** list: every dojo with a checkbox, and inside it every
challenge with its own. Uncheck one and learners no longer see it: it leaves the dojo, the profile, the belt
counts and `./academy`, and it cannot be started; a dojo with every challenge off disappears and stops blocking
the next belt. Check it again to bring it back; progress is kept. The switches live in
`.academy-data/disabled.json`, apply to the classroom server too, and `scripts/pack_portable.sh` copies them
into the tarball.

Admin mode is password protected. The first `./run.sh` asks you to set the admin password (Enter skips; the first
admin run then asks instead), and every admin run asks for it in the terminal. Only a salted hash is stored, in
`.academy-data/admin.json`. Change it with `./academy admin --change-password`. Forgot it? Run
`./academy admin --reset-password` (or delete that file) and the next admin run sets a new one.
`scripts/pack_portable.sh` copies the hash into the tarball so learner copies stay locked. Anyone who can edit this
folder can also reset the password, so it keeps learners out of admin mode, not someone with your files.

## Instructor answers guide

Every challenge has a worked answer, and a script proves each one still passes its own check:

```bash
python3 scripts/verify_answers.py --json dist/verify.json      # fresh copy of each challenge, answer applied, ./check run
python3 scripts/build_answers_guide.py --report dist/verify.json --pdf   # dist/signal-dojo-answers.pdf
```

The answers live in each challenge's `solution/` folder (plus `solve.sh` for the commands a learner types), and the
walkthroughs in `docs/answers/`. Neither ships in the learner tarball.

## Classroom

`./run.sh` (or `./academy serve --host <LAN IP>`) serves the whole class with logins and an optional shared git repo for progress. See [docs/CLASSROOM.md](docs/CLASSROOM.md).

## Notes

- Instructor solutions live in `solution/` next to each `files/`; they never reach learners and are left out of the tarball unless `INCLUDE_SOLUTIONS=1`.
- The Linux shell modules are adapted from pwn.college Linux Luminarium (BSD 2-Clause).
- No lesson links to the internet. `scripts/check_curriculum.py` fails on any outside link in a challenge.

```text
run.sh  academy  curriculum/  platform/  vendor/  scripts/  docs/
```
