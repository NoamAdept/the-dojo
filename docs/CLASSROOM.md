# One server for a whole class

One machine runs The Dojo. Learners only need a browser.

```bash
./run.sh
```

It prints the address for learners, for example `http://192.168.1.50:8080/`.
Each learner presses **Create account** once, then **Log in**.
Their files are on the server in `~/dojo/<name>`. They work there at the server or over SSH.

## Accounts

```bash
./academy user add NAME      # make an account
./academy user passwd NAME   # reset a password
```

To stop learners from making their own accounts, start it with `./academy serve --host 0.0.0.0 --no-signup`.

## Save progress to git (optional)

```bash
./academy serve --host 0.0.0.0 --progress-repo /srv/class-progress
```

`/srv/class-progress` is a clone of a git repo where `git push` works with no password.
After each change, The Dojo saves `progress/<name>.json` there and pushes it. With no network, it tries again every minute.

## Safety

All learners use the server's OS account, so they can read each other's files.
Use a separate Pi, VM or container, on a trusted network (it is plain http).
