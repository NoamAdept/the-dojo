# The Dojo

Learn the terminal, C++ and Python from zero. Works offline. 4 belts, 110 challenges.
You only need `python3`.

## Start

```bash
tar -xzf the-dojo.tar.gz
cd the-dojo
./run.sh
```

Open the address it prints. Press **Create account**, then **Log in**.

**Windows:** use WSL. See [docs/WSL.md](docs/WSL.md).

## Solve a challenge

1. Press **Read lesson**, then **Start**. Your files are in `~/dojo/<your name>`.
2. Do the tasks in `README.md`. Run `./check`.
3. When it prints `CHECK_OK`, press **Mark as done**.

Stuck? Press **Hint**. Your progress saves by itself.

## Belts

| Belt | You learn |
|------|-----------|
| White | The terminal |
| Yellow | Linux: processes, permissions, scripts |
| Orange | C++ |
| Blue | Python |

## For the admin

| To do this | Type this |
|------------|-----------|
| Make the tarball (no answers in it) | `./scripts/pack_portable.sh` |
| Reset a learner's password | `./academy user passwd NAME` |
| Open any challenge | `ACADEMY_ADMIN=1 ./run.sh` |
| Test every answer | `python3 scripts/verify_answers.py` |
| Make the answers PDF | `python3 scripts/build_answers_guide.py --pdf` |

- The answers are in [docs/answers](docs/answers) and each challenge's `solution/` folder. They are not in the tarball.
- Changed a `solution/`? Run `python3 scripts/build_answers_guide.py --md` to update docs/answers.
- One server for a whole class: [docs/CLASSROOM.md](docs/CLASSROOM.md).
- Tools for a Linux lab machine:

  ```bash
  sudo apt install vim tmux curl less man-db manpages-dev build-essential gdb cmake \
    pkg-config git tree net-tools netcat-openbsd iproute2 lsof procps psmisc
  ```

The Linux shell lessons are adapted from pwn.college Linux Luminarium (BSD 2-Clause).
