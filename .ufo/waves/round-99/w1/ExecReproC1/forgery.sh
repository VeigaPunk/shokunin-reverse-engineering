#!/bin/bash
# ExecReproC1 — rebuild the C1 forgery control at B0 in a fixture commit (clone only).
set -u
S=/fast/scratch/hyaku/kaidoku-r99/ExecReproC1
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ExecReproC1
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
mkdir -p "$S" "$W"
trap 'rm -rf -- "$S/clone-f"' EXIT
git clone --shared -q "$LANE" "$S/clone-f" || exit 9
git -C "$S/clone-f" checkout --detach de098f51cd73d3b9b4a895840da8f2bb0a386db8 || exit 9
test "$(git -C "$S/clone-f" rev-parse --show-toplevel)" = "$S/clone-f" || { echo "toplevel-mismatch"; exit 9; }
cp "$LANE/.ufo/waves/round-99/pre/c1-forgery-control.diff" "$W/c1-forgery-control.diff"
git -C "$S/clone-f" apply --whitespace=nowarn "$W/c1-forgery-control.diff" \
  || git -C "$S/clone-f" apply --3way "$W/c1-forgery-control.diff" || { echo "apply-failed"; exit 8; }
git -C "$S/clone-f" -c user.name=fixture -c user.email=fixture@fixture.invalid commit -qam "fixture: round-99 C1 forgery control" || exit 8
FIX=$(git -C "$S/clone-f" rev-parse HEAD)
echo "fixture=$FIX"
cd "$S/clone" || exit 9
python3 -I -B tools/round-99/self-assessment-audit.py --root "$S/clone-f" --rev "$FIX" --json-out "$W/c1-forgery.repro.json"
echo "forgery rc=$?"
