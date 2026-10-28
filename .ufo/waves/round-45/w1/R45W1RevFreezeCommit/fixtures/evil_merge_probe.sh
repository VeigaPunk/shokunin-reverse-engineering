#!/usr/bin/env bash
# F1 probe: an evil merge whose OWN resolution is the only writer of a frozen path.
# Builds a throwaway repo under $TMPDIR, then asks both arms the same question.
set -uo pipefail
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
PF=${PF:-$L/tools/round-45/frozen-path-preflight.py}
D=$(mktemp -d -p "${TMPDIR:-/tmp}") && git -C "$D" init -q
git -C "$D" config user.email "fixture@r45"; git -C "$D" config user.name "r45 fixture"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "TOPLEVEL_MISMATCH"; exit 9; }
mkdir -p "$D/frozen"; echo v0 > "$D/frozen/target.txt"; echo p > "$D/a.txt"; echo q > "$D/b.txt"
git -C "$D" add -A; git -C "$D" commit -qm freeze
FZ=$(git -C "$D" rev-parse HEAD); MAIN=$(git -C "$D" symbolic-ref --short HEAD)
git -C "$D" checkout -q -b side; echo p1 > "$D/a.txt"; git -C "$D" add -A; git -C "$D" commit -qm "side: a.txt"
git -C "$D" checkout -q "$MAIN";  echo q1 > "$D/b.txt"; git -C "$D" add -A; git -C "$D" commit -qm "trunk: b.txt"
git -C "$D" merge -q --no-ff side -m "merge side" || true
echo EVIL > "$D/frozen/target.txt"; git -C "$D" add -A; git -C "$D" commit -q --amend --no-edit
H=$(git -C "$D" rev-parse HEAD)
echo "fixture=$D"; echo "FREEZE=$FZ"; echo "HEAD=$H (merge: parents=$(( $(git -C "$D" rev-list --parents -n1 $H | wc -w) - 1 )))"
echo "frozen/target.txt at freeze = '$(git -C "$D" show $FZ:frozen/target.txt)'  blob=$(git -C "$D" rev-parse $FZ:frozen/target.txt)"
echo "frozen/target.txt at HEAD   = '$(cat "$D/frozen/target.txt")'  blob=$(git -C "$D" rev-parse $H:frozen/target.txt)"
echo
echo "--- arm 1: preflight (git log -m --diff-merges=first-parent + blob arm) ---"
python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$H" --pathspec frozen/ --freeze-path frozen; echo "PREFLIGHT_EXIT=$?"
echo
echo "--- arm 2: both counters' frozen_path_changed (git log --name-only, no -m) ---"
python3 -I -B - "$D" "$FZ" "$H" "$L" <<'PY'
import importlib.util, sys
root, fz, h, L = sys.argv[1:5]
for p in ("c1-counter.py", "c2-counter.py"):
    spec = importlib.util.spec_from_file_location("m_" + p, L + "/tools/round-45/" + p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.FROZEN = ["frozen"]                      # point the arm at the fixture's frozen path
    print(p, "->", repr(m.frozen_path_changed(root, fz, h)))
PY
echo
echo "--- raw git, same range, same pathspec ---"
echo -n "log --name-only (counter form): "; git -C "$D" log --name-only --format= "$FZ..$H" -- frozen/ | tr '\n' ' '; echo "(none above = invisible)"
echo -n "log -m --name-status (preflight form): "; git -C "$D" log -m --diff-merges=first-parent --name-only --format= "$FZ..$H" -- frozen/ | tr '\n' ' '; echo
rm -rf -- "$D"
