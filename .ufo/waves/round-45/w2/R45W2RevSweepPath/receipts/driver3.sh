#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RevSweepPath
PF=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-45/frozen-path-preflight.py
say(){ printf '\n### %s\n' "$*"; }
run(){ printf '$ %s\n' "$*"; "$@"; printf 'rc=%s\n' "$?"; }
D=$S/fx6-scope; rm -rf "$D"; git init -q "$D"; cd "$D" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$D" ] && echo toplevel_ok
mkdir -p tools/round-45 other
echo one > tools/round-45/frozen.txt; echo base > other/base.txt
git add -A; git -c user.name=u -c user.email=u@x commit -qm base
FZ=$(git rev-parse HEAD); echo "freeze=$FZ"
echo two > other/later.txt; git add -A; git -c user.name=u -c user.email=u@x commit -qm later
REV=$(git rev-parse HEAD); echo "rev=$REV"
say "fx6a: dirty INSIDE the named frozen pathspec"
echo dirty >> tools/round-45/frozen.txt
run python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty
git checkout -- tools/round-45/frozen.txt
say "fx6b: dirty OUTSIDE the named frozen pathspec (round-44 fixtures dirty while round 45 scores)"
echo dirty > other/uncommitted.txt
run python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty
run python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty --dirty-pathspec other/
say "fx6c: the same tree, no --check-dirty"
run python3 -I -B "$PF" --root "$D" --freeze "$FZ" --rev "$REV" --pathspec tools/round-45/ --freeze-path tools/round-45
