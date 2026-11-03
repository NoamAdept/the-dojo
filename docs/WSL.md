# The Dojo on Windows (WSL)

On Windows laptops and desktops, The Dojo runs inside **WSL** (Windows Subsystem for Linux) with
**Ubuntu 24.04**. Each learner runs their own copy on their own machine and uses it in their Windows browser.
Nothing needs the internet on the learner's machine.

| Piece | Where it runs |
|-------|---------------|
| `./run.sh`, the challenge folder, `./check`, vim, g++, gdb, Python | Ubuntu (WSL) |
| The Dojo page | Any Windows browser at `http://localhost:8080/` |
| The terminal **Start** opens | Windows Terminal (or a console window), already inside Ubuntu |

## Fastest path: the prepared image (air-gapped)

The admin builds one Ubuntu image with every package and the academy in it, once, on a PC with internet.
Learner machines then only need that one file. No `apt`, no pip, no internet.

### Build the image (admin, once, with internet)

1. In PowerShell: `wsl --install -d Ubuntu-24.04`. Make a user, for example `learner`.
2. In the Ubuntu window:

   ```bash
   tar -xzf /mnt/c/Users/YOU/Downloads/the-dojo.tar.gz -C ~
   sh ~/the-dojo/wsl/build-image.sh
   ```

   It installs the lab packages (vim, tmux, man pages, g++, gdb, cmake, net tools), makes vim the editor,
   turns on systemd, makes `learner` the default user and adds the `dojo` command. It fails loudly if
   any tool is missing.
3. Optional: `cd ~/the-dojo && ACADEMY_ADMIN=1 ./run.sh` once to set the admin password, so every copy
   shares it. Stop it with Ctrl-C.
4. In PowerShell:

   ```powershell
   wsl --shutdown
   wsl --export Ubuntu-24.04 the-dojo-wsl.tar
   ```

5. Copy `the-dojo-wsl.tar` and `the-dojo/wsl/install-the-dojo.ps1` to a USB stick or a share.

### Install it on each laptop (no internet)

```powershell
powershell -ExecutionPolicy Bypass -File .\install-the-dojo.ps1
```

This imports the image as the WSL distro **TheDojo** and puts a **The Dojo** shortcut on the desktop.
Double-click it: the academy starts and the browser opens at `http://localhost:8080/`.
By hand: `wsl -d TheDojo`, then `dojo`.

### Install WSL without internet

Skip this if `wsl --status` already works.

1. On a PC with internet, download the WSL installer `wsl.<version>.x64.msi` (or `arm64`) from
   the Releases page of github.com/microsoft/WSL.
2. On the laptop, in an **admin** PowerShell:

   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   msiexec /i wsl.2.x.x.x64.msi /quiet
   ```

3. Restart Windows. Virtualization must be on in the BIOS/UEFI (it is on most laptops).

## Other path: plain Ubuntu on WSL plus the tarball

When the laptops can reach an apt mirror (or the internet) once:

```bash
# in Ubuntu (WSL), as your normal user
cd ~ && tar -xzf /mnt/c/Users/YOU/Downloads/the-dojo.tar.gz
sh ~/the-dojo/wsl/setup-ubuntu.sh
# then in PowerShell: wsl --shutdown   (so systemd starts), open Ubuntu again
dojo
```

## Rules that keep every challenge working

- **Unpack inside Ubuntu, in your Linux home (`~`), with `tar`.** Not in `C:\` / `/mnt/c/...`, and not with
  Windows Explorer or 7-Zip. Windows folders drop Linux permissions and the executable bit, so `./check`,
  `./run` and the permission challenges break there. `./run.sh` refuses to start from `/mnt/c/...` and says so.
- **Your challenge files are in `~/dojo/<your username>`.** That is a link to
  `~/the-dojo/.academy-data/classroom/users/<username>/challenge`, the folder **Start** fills.
  Open it with `cd ~/dojo/<username>`. The page shows the same path after **Start**.
- **Stay in the challenge folder itself when you press Start.** Start empties the folder and fills it again.
  A terminal sitting inside one of its subfolders (for example `framer/`) is left in a folder that no longer
  exists and `ls` shows nothing: run `cd ~/dojo/<username>` again.
- From Windows, the files are at `\\wsl$\TheDojo\home\learner\dojo\` in Explorer (read them,
  but edit in vim inside Ubuntu: Windows editors can add CRLF line endings that break shell scripts).

## How The Dojo behaves on WSL

`./run.sh` notices WSL by itself:

- It listens on `127.0.0.1` (this laptop only) and prints `http://localhost:8080/`. Windows forwards
  `localhost` into WSL, so any Windows browser works. `HOST=0.0.0.0 ./run.sh` opens it to the network, but
  other computers reach WSL only with WSL's mirrored networking (`networkingMode=mirrored` in `.wslconfig`)
  or a `netsh portproxy` rule.
- It opens the Windows browser by itself (`OPEN_BROWSER=0 ./run.sh` turns that off).
- **Start** opens a Windows Terminal tab (or a console window when Windows Terminal is not installed) in the
  challenge folder, inside the same Ubuntu.
- Logged-in learners can use the terminal commands with their own account:
  `ACADEMY_USER=<username> ./academy hint`, `ACADEMY_USER=<username> ./academy status`.

## Checking a machine

```bash
cd ~/the-dojo
python3 scripts/verify_answers.py --classroom   # only in a checkout with solution/ folders (instructor copy)
```

It stages every challenge the way a logged-in learner gets it, checks that every file is where the lesson
and `./check` expect it, then proves each answer passes. On Ubuntu 24.04 with the packages above all 110 pass.

## Troubleshooting

| You see | Fix |
|---------|-----|
| `The Dojo is in a Windows folder` | Unpack in `~` (see above). |
| `/bin/sh^M: bad interpreter` | The tarball was unpacked on the Windows side. Unpack it again inside Ubuntu with `tar`. |
| The page does not open at `localhost:8080` | Is `./run.sh` still running in the Ubuntu window? Try `http://127.0.0.1:8080/`. |
| No terminal opens on Start | Open Ubuntu yourself and `cd ~/dojo/<username>`. |
| `systemctl` says systemd is not running | `wsl --shutdown` in PowerShell, then open Ubuntu again (the setup turns systemd on). |
