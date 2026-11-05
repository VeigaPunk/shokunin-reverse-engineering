#!/bin/sh
# Round-92 L1 measurement at a given revision (frozen counters; no counter is edited).
# usage: measure-at-rev.sh <rev-short-or-full> <scratch-dir>
# Run from the lane root. Receipts land in .ufo/waves/round-92/l1/scores/.
set -u
REV="$1"; S="$2"; OUT=.ufo/waves/round-92/l1/scores
mkdir -p "$S/tmp" "$S/work" "$OUT"
export TMPDIR="$S/tmp"
C="$(pwd)"
CAND=tools/round-92/upx-stop-boundary-search-repair.py
C1="repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10"
V2="refused 10 of 10; typed 10; unsafe 0; intact 5 of 5"
REG="P1 6 of 6; P2 4 of 4; P3 4 of 4"
echo "selftest candidate: $(python3 -I -B $CAND --selftest >/dev/null 2>&1; echo rc=$?)"
python3 -I -B tools/round-92/stop-boundary-repair-battery.py --root . --repair-cmd $CAND --work "$S/work/c1" --rev "$REV" --expect "$C1" --json-out "$OUT/c1-at-$REV.json"; echo "c1 rc=$?"
python3 -I -B tools/round-92/stop-boundary-battery-v2.py --root . --repair-cmd tools/round-91/upx-stop-boundary-repair.py --work "$S/work/c2pos" --rev "$REV" --expect "$V2" --json-out "$OUT/c2-positive-v2-round91-at-$REV.json"; echo "c2 positive rc=$?"
for k in A B C; do
  case $k in A) f=cheat_carrier_read.py;; B) f=cheat_hash_table.py;; C) f=cheat_typed_only.py;; esac
  python3 -I -B tools/round-92/stop-boundary-battery-v2.py --root . --repair-cmd "$C/.ufo/waves/round-92/controls/$f" --work "$S/work/c2$k" --rev "$REV" --expect "$V2" --json-out "$OUT/c2-counterfeit-$k-v2-at-$REV.json"; echo "c2 counterfeit $k rc=$?"
done
python3 -I -B tools/round-90/upx-later-block-battery.py --root . --repair-cmd $CAND --work "$S/work/reg" --rev "$REV" --expect "$REG" --json-out "$OUT/regress-candidate-at-$REV.json"; echo "regress rc=$?"
