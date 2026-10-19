#!/usr/bin/env bash
# EX-24 (chain c3, arc3-loop1-round4) — build the mkdir-guard injection variants.
#
# Base revision: .ufo/gates/custody-pair/custody-pair.py sha256
#   7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09 (1155 lines)
#   -- read from the repo, NEVER written. All variants land under /var/tmp.
#
# Produces, under /var/tmp/ex24-r4/:
#   variants/after/    — the injection: out.parent.mkdir moved inside the guarded try
#   variants/sabotage/ — the injection REVERTED (selftest arms must catch it)
#   variants/flag-only/— alternative shape: explicit is_dir() pre-check, USAGE (kept out of after/)
set -euo pipefail

REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SRC="$REPO/.ufo/gates/custody-pair/custody-pair.py"
D=/var/tmp/ex24-r4
V="$D/variants"

EXPECT=7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09
got=$(sha256sum "$SRC" | cut -d' ' -f1)
[ "$got" = "$EXPECT" ] || { echo "REFUSING: base revision moved: $got != $EXPECT" >&2; exit 1; }

rm -rf "$V"; mkdir -p "$V/after" "$V/sabotage" "$V/flag-only"

# ---- after: move the mkdir into the guarded region -------------------------
python3 - "$SRC" "$V/after/custody-pair.py" <<'PY'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
text = pathlib.Path(src).read_text(encoding="utf-8")
old = """        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")
"""
new = """        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
"""
assert text.count(old) == 1, "anchor for the mkdir move not unique: %d" % text.count(old)
pathlib.Path(dst).write_text(text.replace(old, new), encoding="utf-8")
PY

# ---- sabotage: the injection reverted (byte-identical to the base) ---------
python3 - "$SRC" "$V/sabotage/custody-pair.py" <<'PY'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
text = pathlib.Path(src).read_text(encoding="utf-8")
pathlib.Path(dst).write_text(text, encoding="utf-8")
PY

# ---- flag-only: explicit is_dir pre-check (declared-shape alternative) -----
python3 - "$SRC" "$V/flag-only/custody-pair.py" <<'PY'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
text = pathlib.Path(src).read_text(encoding="utf-8")
old = """        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")
"""
new = """        if out.parent != out and not out.parent.is_dir():
            print("USAGE: refusing to write a receipt: parent is not a directory: %s" % out.parent,
                  file=sys.stderr)
            return EXIT_USAGE
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")
"""
assert text.count(old) == 1, "anchor for the flag-only variant not unique"
pathlib.Path(dst).write_text(text.replace(old, new), encoding="utf-8")
PY

for v in after sabotage flag-only; do
  chmod +x "$V/$v/custody-pair.py"
  printf '%-10s %s  lines=%s\n' "$v" "$(sha256sum "$V/$v/custody-pair.py" | cut -d' ' -f1)" "$(wc -l < "$V/$v/custody-pair.py")"
done
diff -u "$SRC" "$V/after/custody-pair.py" > "$V/after.diff" || true
diff -u "$SRC" "$V/flag-only/custody-pair.py" > "$V/flag-only.diff" || true
echo "diffs: $V/after.diff ($(wc -l < "$V/after.diff") lines), $V/flag-only.diff ($(wc -l < "$V/flag-only.diff") lines)"
