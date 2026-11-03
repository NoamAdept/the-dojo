<#
  Signal Dojo: install the prepared WSL image on one Windows laptop or desktop, with no internet.

  Put these next to this script (on a USB stick or a share):
    signal-dojo-wsl.tar      the Ubuntu image your admin exported (docs/WSL.md, "Build the image")

  Then, in PowerShell (no admin rights needed once WSL itself is installed):
    powershell -ExecutionPolicy Bypass -File .\install-signal-dojo.ps1

  It imports the image as the WSL distro "SignalDojo" under %LOCALAPPDATA%\SignalDojo and puts a
  "Signal Dojo" shortcut on the desktop that starts the academy and opens it in the browser.
#>
param(
  [string]$Image = (Join-Path $PSScriptRoot "signal-dojo-wsl.tar"),
  [string]$Name = "SignalDojo",
  [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "SignalDojo")
)
$ErrorActionPreference = "Stop"

function Fail($msg) { Write-Host $msg -ForegroundColor Red; exit 1 }

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
  Fail "WSL is not installed. See docs/WSL.md, 'Install WSL without internet', then run this again."
}
& wsl.exe --status *> $null
if ($LASTEXITCODE -ne 0) {
  Fail "WSL is not ready (wsl --status failed). Install it (docs/WSL.md) and restart Windows, then run this again."
}
if (-not (Test-Path $Image)) { Fail "Image not found: $Image" }

# wsl --list prints UTF-16; normalise before matching.
$existing = (& wsl.exe --list --quiet) -replace "`0", "" | Where-Object { $_.Trim() -eq $Name }
if ($existing) {
  Write-Host "$Name is already installed. To replace it: wsl --unregister $Name (this deletes its files), then run this again."
} else {
  New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
  Write-Host "Importing $Image as $Name (a few minutes)..."
  & wsl.exe --import $Name $InstallDir $Image --version 2
  if ($LASTEXITCODE -ne 0) { Fail "wsl --import failed." }
}

# Desktop shortcut: starts Signal Dojo in its own window; run.sh opens the browser by itself.
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desktop "Signal Dojo.lnk"))
$lnk.TargetPath = (Get-Command wsl.exe).Source
$lnk.Arguments = "-d $Name --cd ~ -- bash -lc ""signal-dojo"""
$lnk.Description = "Start Signal Dojo"
$lnk.Save()

Write-Host ""
Write-Host "Done. Double-click 'Signal Dojo' on the desktop (or run: wsl -d $Name), then"
Write-Host "open http://localhost:8080/ if the browser does not open by itself."
