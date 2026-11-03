# Classroom server

One machine serves the whole lab; learners only need a browser.

**Admin** (from the tarball or a checkout, python3 only):

```bash
./academy serve --host 192.168.1.50            # this machine's LAN IP (or 0.0.0.0); port 8080
./academy serve --host 192.168.1.50 --port 9000 --data /srv/academy \
                --progress-repo /srv/class-progress --no-signup
./academy user add alice                        # make an account (prompts for the password)
./academy user passwd alice                     # reset a password
```

- `--data DIR` holds `users.json` (salted PBKDF2 hashes, never in git) and `users/<name>/`
  (each learner's `challenge/` folder, progress and flag). Default: `.academy-data/classroom/`.
- `--no-signup` turns off self-registration; then only `academy user add` creates accounts.
- `./run.sh` starts this classroom server on all network interfaces (`HOST=0.0.0.0`, port 8080) and prints the
  address to give learners. `HOST=127.0.0.1 ./run.sh` keeps it to this machine. `SINGLE_USER=1 ./run.sh` is the old
  no-login console with one local `~/signal-dojo/challenge` folder (`academy serve --local`).
- Folders are private to the server's OS account (`chmod 700` on the data folder, `users/` and each `users/<name>/`).
  Logins are kept as sha256 hashes in `sessions.json` (0600), so restarting the server does not log anyone out.

**Learners** open `http://192.168.1.50:8080/`. The first time they choose **Create account** (username and a
password of 8+ characters, typed twice); after that they **Log in**. Logging in to a name that has no account is
refused, so a typo never starts an empty account. Progress saves by itself to `users/<name>/.academy/progress.json`
on every start, hint and solve. Then they press Start. The page shows the path of their own challenge folder on the server
(`users/<name>/challenge`, linked as `~/signal-dojo/<name>` for the server's OS account); they open a terminal there (sitting at the server, a terminal window
pops up by itself; from another machine, over SSH). Start → solve → Done. Logins last 12 hours and survive a server restart.

**Shared progress repo** (optional). Make a GitHub repo, clone it on the server and make sure
`git push` works there non-interactively (deploy key with write access, or a credential helper):

```bash
git clone git@github.com:your-org/class-progress.git /srv/class-progress
cd /srv/class-progress && git commit --allow-empty -m init && git push -u origin HEAD   # if empty
```

Then pass `--progress-repo /srv/class-progress`. After each change the server writes
`progress/<username>.json` (per challenge: solved, started/completed time, hints, attempts —
no flags, passwords or paths), commits it as `<username> <username@academy.local>`, and runs
`git pull --rebase` + `git push` in the background a few seconds later. If the lab is offline
the commits wait locally and the push is retried every minute. A learner logging in on a fresh
server gets their progress restored from `progress/<username>.json`.

**Caveat: every learner's folder belongs to the server's OS account.** Learners can read each
other's folders, the hashes in `users.json`, and anything else that account can. Run the
server on a dedicated Pi, VM or container under a plain (non-root) user, on a trusted lab
network (it is plain http).
