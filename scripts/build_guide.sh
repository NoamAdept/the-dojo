#!/bin/sh
# Render docs/guide/guide.html to the one-page PDF docs/signal-dojo-guide.pdf.
# Needs a Chromium or Chrome binary (set CHROME=... if it is not on PATH).
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
CHROME="${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || true)}"
if [ -z "$CHROME" ]; then
  echo "build_guide: no Chromium/Chrome found; set CHROME=/path/to/chrome" >&2
  exit 1
fi
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$ROOT/docs/signal-dojo-guide.pdf" "file://$ROOT/docs/guide/guide.html"
echo "wrote docs/signal-dojo-guide.pdf"
