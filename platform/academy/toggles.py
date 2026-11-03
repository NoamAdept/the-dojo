"""Admin on/off switches for dojos and single challenges.

Stored in <data dir>/disabled.json as {"dojos": [...], "challenges": [...]}.
Everything is on unless listed. A switched-off dojo hides with all its challenges;
a switched-off challenge hides from the dojo, the CLI and the API (learners and admin alike).
The admin page lists everything so it can be switched back on.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

FILENAME = "disabled.json"


class Toggles:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._mtime: float | None = None
        self._dojos: frozenset[str] = frozenset()
        self._challenges: frozenset[str] = frozenset()

    def _refresh(self) -> None:
        # Re-read when the file changes, so every per-user engine and the CLI see the same switches.
        try:
            mtime = self.path.stat().st_mtime
        except OSError:
            mtime = None
        if mtime == self._mtime:
            return
        self._mtime = mtime
        data: dict = {}
        if mtime is not None:
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = {}
        if not isinstance(data, dict):
            data = {}
        self._dojos = frozenset(str(x) for x in data.get("dojos") or [])
        self._challenges = frozenset(str(x) for x in data.get("challenges") or [])

    @property
    def disabled_dojos(self) -> frozenset[str]:
        self._refresh()
        return self._dojos

    @property
    def disabled_challenges(self) -> frozenset[str]:
        self._refresh()
        return self._challenges

    def set(self, kind: str, item_id: str, enabled: bool) -> None:
        if kind not in ("dojo", "challenge"):
            raise ValueError("kind must be 'dojo' or 'challenge'")
        self._refresh()
        dojos, challenges = set(self._dojos), set(self._challenges)
        target = dojos if kind == "dojo" else challenges
        if enabled:
            target.discard(item_id)
        else:
            target.add(item_id)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"dojos": sorted(dojos), "challenges": sorted(challenges)}, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, self.path)
        self._mtime = None  # mtime can tie within one clock tick; force a re-read
