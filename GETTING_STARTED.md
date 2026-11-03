# Getting started (closed network)

You need **python3**. Nothing else. No pip. No internet.

```bash
tar -xzf the-dojo.tar.gz
cd the-dojo
./run.sh
```

Open the URL it prints. Other computers on the same network can open the network address it prints too
(up to about 5 learners at once works well on a Raspberry Pi). `HOST=127.0.0.1 ./run.sh` keeps it to this computer.

1. **Create account**: pick a username and a password. Next time, **Log in** with them.
   Your progress saves by itself to a folder that is only yours (`.academy-data/classroom/users/<username>/`).
2. Read the intro, then **Enter the lab**
3. **Start** → files land in your own folder, `~/dojo/<username>` (a link to
   `.academy-data/classroom/users/<username>/challenge`); on the server itself a terminal opens there
4. Read the README, solve it
5. **Done**

To take a copy of your work with you, press **Save to a file** in the lab: one `.zip` with your progress and your
scripts. `SINGLE_USER=1 ./run.sh` is the old one-learner mode without logins, where **Restore** brings a save file
back. (Terminal: `./academy save`, `./academy restore FILE`.)

**Windows:** run it inside WSL (Ubuntu), unpacked in your Linux home folder, not in `C:\`. See [docs/WSL.md](docs/WSL.md).

If `./run.sh` says it cannot find python3, install only the system `python3` package from your OS media — still no pip.
