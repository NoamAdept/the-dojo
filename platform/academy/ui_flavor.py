"""Creative display titles + generated challenge thumbnails."""

from __future__ import annotations

import hashlib

TITLES: dict[str, str] = {
    "orient-find-flag": "Needle in the Labyrinth",
    "orient-permissions": "The Locked Drawer",
    "orient-process-hunt": "Ghost in the Process List",
    "orient-environment": "Whispered Variables",
    "orient-broken-service": "The Silent Port",
    "orient-system-investigation": "Autopsy of a Pi",
    "cli-pipeline": "Pipe Dream",
    "cli-text-extraction": "Frequencies in the Fog",
    "cli-log-detective": "Receiver Log Noir",
    "cli-shell-automation": "Night Watch Inventory",
    "py-control-flow": "Strength Classifier",
    "py-file-parser": "Config Crypt",
    "py-binary-decoder": "Sensor Bones",
    "py-protocol-parser": "Noisy Frame Tamer",
    "py-socket-client": "Knock on Localhost",
    "py-auto-investigator": "The Autopilot Probe",
    "cpp-compile-it": "First Blood Compile",
    "cpp-pointer-basics": "Follow the Arrow",
    "cpp-memory-layout": "Bytes Under Glass",
    "cpp-binary-parser": "Length-Prefixed Prey",
    "gdb-first-breakpoint": "Stop Right There",
    "gdb-find-variable": "The Moving Target",
    "gdb-follow-stack": "Down the Call Well",
    "gdb-inspect-memory": "Peek Behind the Bytes",
    "gdb-logic-bug": "Wrong Answer, Right Place",
    "gdb-segfault": "The Crash Site",
    "sys-pipes": "Parent, Child, Pipe",
    "sys-file-descriptors": "Copy Through the FD",
    "sys-process-controller": "Puppet the Child",
    "sys-tcp-client": "Local Wire Tap",
    "pyq-collections": "Event Ledger",
    "pyq-modern-python": "Typed Packet Router",
    "cppq-strings-files": "Config That Lasts",
    "cppq-templates": "Generic Decoder Buffer",
    "cppq-modern-cpp": "Modern Channel Scanner",
}


def display_title(challenge_id: str, fallback: str = "") -> str:
    return TITLES.get(challenge_id, fallback or challenge_id)


def _palette(challenge_id: str) -> tuple[str, str, str, str]:
    digest = hashlib.sha256(challenge_id.encode()).digest()
    hues = [digest[i] for i in range(6)]
    a = f"hsl({hues[0] * 360 // 255}, 70%, 48%)"
    b = f"hsl({hues[1] * 360 // 255}, 65%, 38%)"
    c = f"hsl({(hues[2] * 360 // 255 + 40) % 360}, 80%, 58%)"
    ink = "#c8ff00" if digest[3] % 2 == 0 else "#4ecdc4"
    return a, b, c, ink


def challenge_thumb_svg(challenge_id: str) -> str:
    """Tiny unique ‘photo’ — geometric art, unique per challenge id."""
    digest = hashlib.sha256(challenge_id.encode()).digest()
    a, b, c, ink = _palette(challenge_id)
    gid = digest[:4].hex()
    kind = digest[4] % 6
    extras: list[str] = []
    # Soft orbs so each thumb reads like a tiny photo, not a glyph.
    extras.append(
        f'<ellipse cx="{40 + digest[5] % 80}" cy="{28 + digest[6] % 40}" '
        f'rx="{28 + digest[7] % 24}" ry="{18 + digest[8] % 16}" fill="{c}" opacity="0.35"/>'
    )
    extras.append(
        f'<ellipse cx="{90 + digest[9] % 50}" cy="{70 + digest[10] % 30}" '
        f'rx="{20 + digest[11] % 20}" ry="{14 + digest[12] % 14}" fill="#050705" opacity="0.25"/>'
    )
    if kind == 0:
        extras.append(
            f'<path d="M8 {40 + digest[13] % 30} C 28 20, 48 108, 88 {30 + digest[14] % 40} '
            f'S 140 20, 152 64" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round"/>'
        )
    elif kind == 1:
        for i in range(8):
            h = 18 + (digest[5 + i] % 70)
            extras.append(
                f'<rect x="{14 + i * 17}" y="{120 - h}" width="12" height="{h}" rx="2" '
                f'fill="{ink}" opacity="{0.35 + (i % 3) * 0.2}"/>'
            )
    elif kind == 2:
        extras.append(f'<circle cx="58" cy="58" r="22" fill="none" stroke="{ink}" stroke-width="3"/>')
        extras.append(f'<circle cx="102" cy="70" r="16" fill="{c}" opacity="0.85"/>')
        extras.append(f'<circle cx="80" cy="86" r="8" fill="{ink}"/>')
    elif kind == 3:
        extras.append(f'<polygon points="80,18 132,104 28,104" fill="none" stroke="{ink}" stroke-width="3"/>')
        extras.append(f'<circle cx="80" cy="72" r="10" fill="{c}"/>')
    elif kind == 4:
        extras.append(f'<path d="M24 96 L80 24 L136 96" fill="none" stroke="{ink}" stroke-width="4"/>')
        extras.append(f'<rect x="56" y="72" width="48" height="28" rx="4" fill="{c}" opacity="0.8"/>')
    else:
        extras.append(
            f'<path d="M12 90 Q 40 {20 + digest[15] % 40}, 80 70 T 148 {40 + digest[16] % 40}" '
            f'fill="none" stroke="{ink}" stroke-width="3.5" stroke-linecap="round"/>'
        )
        extras.append(f'<rect x="18" y="18" width="28" height="18" rx="3" fill="{ink}" opacity="0.55"/>')
    grain = []
    for i in range(18):
        x = 8 + (digest[(i + 3) % 32] * (i + 7)) % 144
        y = 8 + (digest[(i + 11) % 32] * (i + 3)) % 104
        grain.append(f'<circle cx="{x}" cy="{y}" r="1.1" fill="#f2f7f2" opacity="0.18"/>')
    glyph = "".join(part[0].upper() for part in challenge_id.split("-")[:2])[:2]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120" width="160" height="120">
  <defs>
    <linearGradient id="g{gid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}"/>
      <stop offset="1" stop-color="{b}"/>
    </linearGradient>
  </defs>
  <rect width="160" height="120" fill="url(#g{gid})"/>
  <rect x="6" y="6" width="148" height="108" rx="14" fill="#050705" opacity="0.28"/>
  {''.join(extras)}
  {''.join(grain)}
  <text x="14" y="108" font-family="ui-monospace, Menlo, monospace" font-size="14" fill="#f2f7f2" opacity="0.9">{glyph}</text>
</svg>
'''
