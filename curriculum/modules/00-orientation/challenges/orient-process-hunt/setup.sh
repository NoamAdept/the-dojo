#!/usr/bin/env bash
# Build sealed ./run and ./check; hide checker source outside the challenge folder.
set -euo pipefail
DEST="${1:?workspace dest}"
HERE="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
DATA_DIR="${ACADEMY_DATA:-$HOME/.academy}"
RUNTIME="$DATA_DIR/runtime/orient-process-hunt"
CC="${CC:-cc}"

mkdir -p "$RUNTIME"
cp "$HERE/hidden/check.py" "$RUNTIME/check.py"
chmod 700 "$RUNTIME"
chmod 600 "$RUNTIME/check.py"

cd "$DEST"

# run.c is the helper's source: compiled from hidden/, never shown in the challenge folder.
"$CC" -O2 -o run "$HERE/hidden/run.c"
"$CC" -O2 -DCHECK_SCRIPT=\"$RUNTIME/check.py\" -o check "$HERE/hidden/check_stub.c"
chmod 755 run check

# The README points at report.template for the shape, so it stays next to report.txt.
if [[ ! -f report.txt ]]; then
  cp report.template report.txt
fi

# Remove anything that would leak the checker / old names
rm -f \
  unlock check_answers launch launch.c \
  intel.template intel.txt INCIDENT.txt START_HERE.txt \
  answers.template answers.txt decoy_notes.txt

echo "setup: ./run and ./check ready (checker source not in challenge folder)"
