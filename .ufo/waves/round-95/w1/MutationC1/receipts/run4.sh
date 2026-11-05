#!/bin/bash
# usage: run4.sh X  -> runs checks (i)-(iv) in $S/m/X/clone; logs under $S/logs/X
X=$1
S=/fast/scratch/hyaku/kaidoku-r95/MutationC1
C=$S/m/$X/clone; W=$S/work/$X; LG=$S/logs/$X
mkdir -p "$W" "$LG"
export TMPDIR=$S/tmp
DECL=4bda1d1dd3788973f10e61212b70df18b3b14ea0
BASE=b5331db1fb0ce0bf93695ce1730cf831effef6a9
FROZEN="repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"
cd "$C" || exit 99
python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --selftest --work "$W/n1" > "$LG/i.out" 2> "$LG/i.err"; echo $? > "$LG/i.rc"
python3 -I -B tools/round-95/c1-agreement-v2.py --selftest "$W/n2" > "$LG/ii.out" 2> "$LG/ii.err"; echo $? > "$LG/ii.rc"
python3 -I -B tools/round-95/c1-forgery-refusal.py --selftest "$W/n3" > "$LG/iii.out" 2> "$LG/iii.err"; echo $? > "$LG/iii.rc"
python3 -I -B tools/round-95/c1-forgery-refusal.py --root "$C" --fixtures "$C/.ufo/waves/round-95/forgery" --old-prefix forge --old-counter tools/round-94/c1-receipt-agreement.py --honest-dir "$S/honest" --honest-prefix honest --world-rev "$BASE" --instrument-rev "$DECL" --expect "$FROZEN" --json-out "$W/iv-forgery.json" > "$LG/iv.out" 2> "$LG/iv.err"; echo $? > "$LG/iv.rc"
echo "X=$X i=$(cat $LG/i.rc) ii=$(cat $LG/ii.rc) iii=$(cat $LG/iii.rc) iv=$(cat $LG/iv.rc)"
