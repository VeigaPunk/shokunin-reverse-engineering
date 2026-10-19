#!/usr/bin/env bash
# EX-24 (chain c3, arc3-loop1-round4) — build the fixture (selftest) revision.
#
# Produces, under /var/tmp/ex24-r4/:
#   variants/after2/    — after (mkdir moved into the guarded try) + 2 selftest cases
#   variants/sabotage2/ — the 2 selftest cases WITHOUT the mkdir fix
#                         (the sabotage arm: the new cases must read DIRTY here)
set -euo pipefail

REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SRC="$REPO/.ufo/gates/custody-pair/custody-pair.py"
D=/var/tmp/ex24-r4; V="$D/variants"

EXPECT=7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09
got=$(sha256sum "$SRC" | cut -d' ' -f1)
[ "$got" = "$EXPECT" ] || { echo "REFUSING: base revision moved: $got != $EXPECT" >&2; exit 1; }

mkdir -p "$V/after2" "$V/sabotage2"

CASES_FILE="$REPO/.ufo/waves/arc3-loop1-round4/claims/c3/EX-24/harness/mkdir-cases.py.txt"
CASES=$(cat "$CASES_FILE"; echo)

python3 - "$SRC" "$V/after2/custody-pair.py" "$V/sabotage2/custody-pair.py" "$CASES" <<'PY'
import sys, pathlib
src, dst_after, dst_sab, cases = sys.argv[1:5]
cases = cases.rstrip("\n") + "\n\n"
text = pathlib.Path(src).read_text(encoding="utf-8")

mkdir_old = """        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")
"""
mkdir_new = """        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
"""
anchor = "    passed = sum(1 for _, ok, _ in cases if ok)\n"

assert text.count(mkdir_old) == 1 and text.count(anchor) == 1

pathlib.Path(dst_after).write_text(
    text.replace(mkdir_old, mkdir_new).replace(anchor, cases + anchor), encoding="utf-8")
pathlib.Path(dst_sab).write_text(
    text.replace(anchor, cases + anchor), encoding="utf-8")
PY

for v in after2 sabotage2; do
  chmod +x "$V/$v/custody-pair.py"
  printf '%-10s %s  lines=%s\n' "$v" "$(sha256sum "$V/$v/custody-pair.py" | cut -d' ' -f1)" "$(wc -l < "$V/$v/custody-pair.py")"
done
diff -u "$V/after/custody-pair.py" "$V/after2/custody-pair.py" > "$V/fixture.diff" || true
echo "fixture.diff: $(wc -l < "$V/fixture.diff") lines"
