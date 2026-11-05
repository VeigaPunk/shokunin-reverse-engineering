#!/bin/bash
# ExecReproC1 — independent reproduction of R99-C1 at B0, A, Bk + selftest.
set -u
S=/fast/scratch/hyaku/kaidoku-r99/ExecReproC1
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ExecReproC1
mkdir -p "$S" "$W"
trap 'rm -rf -- "$S"' EXIT
cd "$S/clone" || exit 9
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone" || { echo "toplevel-mismatch"; exit 9; }
test "$(git -C "$S/clone" rev-parse HEAD)" = 8fb5ac4fa8d7b0cb5123b230e5d319a765011066 || { echo "not-at-F"; exit 9; }
for pair in "B0:de098f51cd73d3b9b4a895840da8f2bb0a386db8" \
            "A:64cc3e10c5d615c6454570674a265b7290b8919c" \
            "Bk:c19d57cd2e65a036478b9e78f6c5397dedfb2bcb"; do
  tag="${pair%%:*}"; rev="${pair#*:}"
  python3 -I -B tools/round-99/self-assessment-audit.py --root "$S/clone" --rev "$rev" --json-out "$W/c1-at-$tag.repro.json"
  echo "$tag rc=$?"
done
python3 -I -B tools/round-99/self-assessment-audit.py --selftest > "$W/c1-selftest.repro.txt" 2>&1
echo "selftest rc=$?"
