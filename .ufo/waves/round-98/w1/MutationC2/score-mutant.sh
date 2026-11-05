#!/usr/bin/env bash
# score-mutant.sh NAME — run frozen C2 checker + semantic probe on the mutated counter, then restore.
set -u
S=/fast/scratch/hyaku/kaidoku-r98/MutationC2
C=$S/clone
F=tools/round-98/stop-boundary-repair-battery-v8.py
H=7a9837466d2d4eeb0a8096b71b8033c970ac2c43e00ec6f10cc8dd4f6de08a83
N="$1"
cd "$C" || exit 9
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "TOPLEVEL-MISMATCH"; exit 9; }
M=$(sha256sum "$F" | cut -d' ' -f1)
if [ "$M" = "$H" ]; then echo "NOT-MUTATED $N"; exit 9; fi
cp "$F" "$S/receipts/$N.counter.py"
python3 -I -B tools/round-98/allowlist-check.py --counter "$F" --rev 72346895a35a74af18151b125934fa0c09fe1e3c \
  --work "$S/work/$N" --json-out "$S/receipts/$N.json" > "$S/receipts/$N.stdout" 2>&1
RC=$?
LABEL=$(tail -1 "$S/receipts/$N.stdout")
SEM=$(python3 -I -B "$S/semantic.py" "$F" "$S/work/pristine/public-receipt.json" "$S/receipts/$N-semantic.json" 2>&1 | tail -1)
cp "$S/v8-pristine.py" "$F"
R=$(sha256sum "$F" | cut -d' ' -f1)
if [ "$R" = "$H" ]; then RST=restored-ok; else RST=RESTORE-FAILED; fi
echo "$N | frozen_rc=$RC | $LABEL | semantic: $SEM | $RST"
