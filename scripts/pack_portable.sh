#!/usr/bin/env bash
# Build ONE closed-network tarball: python3 + this folder. No pip. No internet on target.
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
NAME="the-dojo"
OUT="${1:-$ROOT/dist/$NAME}"
rm -rf "$OUT"
mkdir -p "$OUT/vendor" "$OUT/platform" "$OUT/curriculum"

# Prefer the repo's already-vendored pure-Python YAML (no .so / no libyaml).
if [[ -d "$ROOT/vendor/yaml" ]]; then
  cp -a "$ROOT/vendor/yaml" "$OUT/vendor/"
elif [[ -d /usr/lib/python3/dist-packages/yaml ]]; then
  cp -a /usr/lib/python3/dist-packages/yaml "$OUT/vendor/"
elif python3 -c "import yaml,os; print(os.path.dirname(yaml.__file__))" >/tmp/yaml_src.txt 2>/dev/null; then
  cp -a "$(cat /tmp/yaml_src.txt)" "$OUT/vendor/yaml"
else
  echo "Need vendor/yaml (or PyYAML on the build machine) to pack." >&2
  exit 1
fi

# Closed-network safety: drop native extensions and the C-libyaml wrapper.
find "$OUT/vendor" -name '*.so' -delete
find "$OUT/vendor" -name '*.pyd' -delete
rm -f "$OUT/vendor/yaml/cyaml.py"
find "$OUT/vendor" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

cp -a "$ROOT/platform/academy" "$OUT/platform/"
find "$OUT/platform" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find "$OUT/platform" -name '*.pyc' -delete 2>/dev/null || true

cp -a "$ROOT/curriculum/." "$OUT/curriculum/"
find "$OUT/curriculum" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
# Instructor solutions stay out of the learner pack unless asked for (INCLUDE_SOLUTIONS=1).
if [[ "${INCLUDE_SOLUTIONS:-0}" != 1 ]]; then
  find "$OUT/curriculum" -type d -name solution -path '*/challenges/*/solution' -prune -exec rm -rf {} +
fi

cp "$ROOT/run.sh" "$OUT/run.sh"
cp "$ROOT/academy" "$OUT/academy"
chmod +x "$OUT/run.sh" "$OUT/academy"
cp "$ROOT/LICENSE" "$OUT/LICENSE" 2>/dev/null || true
cp "$ROOT/README.md" "$OUT/README.md"
mkdir -p "$OUT/docs" && cp "$ROOT/docs/CLASSROOM.md" "$ROOT/docs/WSL.md" "$ROOT/docs/the-dojo-guide.pdf" "$OUT/docs/"
# Windows laptops: WSL setup, image build and offline installer (docs/WSL.md).
cp -a "$ROOT/wsl" "$OUT/wsl" && chmod +x "$OUT/wsl/"*.sh
# Ship the instructor's admin password (salted hash only) so learner copies stay locked.
if grep -q '"hash"' "$ROOT/.academy-data/admin.json" 2>/dev/null; then
  mkdir -p "$OUT/.academy-data" && cp "$ROOT/.academy-data/admin.json" "$OUT/.academy-data/admin.json"
fi
# Dojos and challenges switched off on /admin stay off in learner copies.
if [ -f "$ROOT/.academy-data/disabled.json" ]; then
  mkdir -p "$OUT/.academy-data" && cp "$ROOT/.academy-data/disabled.json" "$OUT/.academy-data/disabled.json"
fi

cat > "$OUT/START_HERE.txt" <<'EOF'
THE DOJO - START HERE

You only need python3. No internet.

  tar -xzf the-dojo.tar.gz
  cd the-dojo
  ./run.sh

Open the address it prints. Press Create account, then Log in.
Your files are in ~/dojo/<your name>.

Windows: use WSL. Read docs/WSL.md.
One server for a whole class: read docs/CLASSROOM.md.
EOF

cp "$OUT/START_HERE.txt" "$OUT/README.txt"

mkdir -p "$ROOT/dist"
TAR="$ROOT/dist/${NAME}.tar.gz"
tar -C "$(dirname "$OUT")" -czf "$TAR" "$(basename "$OUT")"

# Smoke-test the packed tree in isolation (no site-packages).
SMOKE=$(mktemp -d)
trap 'rm -rf "$SMOKE"' EXIT
tar -xzf "$TAR" -C "$SMOKE"
(
  cd "$SMOKE/$NAME"
  export PYTHONNOUSERSITE=1
  export PYTHONPATH="$PWD/vendor:$PWD/platform"
  python3 - <<'PY'
import sys
from pathlib import Path
# Drop host site/dist packages so we only see the pack.
sys.path = [p for p in sys.path if "site-packages" not in p and "dist-packages" not in p]
sys.path[:0] = ["vendor", "platform"]
import yaml
import academy
from academy.dojos import catalog_payload
from academy.engine import AcademyEngine
from academy.classroom import Classroom
from pathlib import Path
import tempfile
assert "vendor" in yaml.__file__.replace("\\", "/")
eng = AcademyEngine(Path("curriculum"), Path(tempfile.mkdtemp()))
assert catalog_payload(eng)["next_challenge"]["id"]
assert len(eng.challenges) == len(list(Path("curriculum").glob("modules/*/challenges/*/challenge.yaml")))
print("smoke ok:", yaml.__file__)
PY
  ./academy serve --help >/dev/null
)

echo "Packed $OUT"
echo "Tarball $TAR ($(du -h "$TAR" | awk '{print $1}'))"
echo "Closed-network: copy the .tar.gz, extract, ./run.sh"
