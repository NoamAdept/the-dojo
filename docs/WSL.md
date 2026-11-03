# The Dojo on Windows (WSL)

The Dojo runs in Ubuntu inside WSL. Learners use it in the Windows browser at `http://localhost:8080/`.
The laptops do not need the internet.

## 1. Make the image (admin, once, on a PC with internet)

In PowerShell:

```powershell
wsl --install -d Ubuntu-24.04
```

Make the user `learner`. Then in Ubuntu (change `YOU` to your Windows user name):

```bash
tar -xzf /mnt/c/Users/YOU/Downloads/the-dojo.tar.gz -C ~
sh ~/the-dojo/wsl/build-image.sh
```

In PowerShell:

```powershell
wsl --shutdown
wsl --export Ubuntu-24.04 the-dojo-wsl.tar
```

Copy `the-dojo-wsl.tar` and `the-dojo/wsl/install-the-dojo.ps1` to a USB stick.

## 2. Install on each laptop (no internet)

In PowerShell, in the USB folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-the-dojo.ps1
```

Then double-click **The Dojo** on the desktop. Or type `wsl -d TheDojo`, then `dojo`.

**No WSL on the laptop?** On a PC with internet, download `wsl.<version>.x64.msi` from
github.com/microsoft/WSL/releases. On the laptop, in PowerShell as administrator:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
msiexec /i wsl.2.x.x.x64.msi /quiet
```

Restart Windows.

## Rules

- Unpack with `tar` inside Ubuntu, in `~`. Never in `C:\`, never with Windows Explorer or 7-Zip.
- Edit files with vim inside Ubuntu.
- Your files are in `~/dojo/<your name>`.
- `wsl --unregister TheDojo` deletes everything, including all the learners' work.

## Problems

| You see | Do this |
|---------|---------|
| `The Dojo is in a Windows folder` | Unpack again inside Ubuntu, in `~`. |
| `/bin/sh^M: bad interpreter` | Unpack again inside Ubuntu, in `~`. |
| The page does not open | Is the black window still open? Try `http://127.0.0.1:8080/`. |
| `Port 8080 is already in use` | An old copy is running. Close it, then start again. |
| No terminal opens after Start | `wsl -d TheDojo`, then `cd ~/dojo/<your name>`. |
| `systemd is not running` | `wsl --shutdown` in PowerShell, then start again. |

**Other way, for laptops with internet:** install Ubuntu, unpack the tarball in `~`, run
`sh ~/the-dojo/wsl/setup-ubuntu.sh`, then `wsl --shutdown`. Open Ubuntu again and type `dojo`.
