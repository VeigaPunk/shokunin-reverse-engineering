#!/usr/bin/env bash
# RV-8 post-landing consumer-shape harness. Run after EX-16 lands the guard.
# Read-only over the repo; scratch under /var/tmp/rv8.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
W=/var/tmp/rv8/post
rm -rf $W && mkdir -p $W/tmp $W/scratch
cp -r $G $W/citation-drift
P=$W/citation-drift/citation-drift-probe.py
T=$W/citation-drift/pointer-table.json
E=$W/citation-drift/expected.json
export TMPDIR=$W/tmp
OUT=$W/post-transcripts.txt
{
echo "### RV-8 post-landing harness $(date -Is)"
echo "### HEAD: $(git -C $REPO rev-parse HEAD)"
echo "### landed gate sha256:"
sha256sum $G/citation-drift-probe.py $G/pointer-table.json $G/expected.json
echo
echo "### P1 default recipe, repo CWD, SKILL.md relative spellings"
( cd $REPO && python3 $P --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json ) | tail -1
echo "P1 rc=${PIPESTATUS[0]}"
echo
echo "### P2 + --strict"
( cd $REPO && python3 $P --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json --strict ) | tail -1
echo "P2 rc=${PIPESTATUS[0]}"
echo
echo "### P3 selftest (expect 13 cases if claim holds)"
python3 $P --selftest --expected $E | tail -2
echo "P3 rc=${PIPESTATUS[0]}"
echo
echo "### P4 byte-identical table copy + committed expected (archived-copy consumer shape)"
cp $T $W/scratch/table-identical.json
python3 $P --root $REPO --rev HEAD --table $W/scratch/table-identical.json --expected $E | tail -1
echo "P4 rc=${PIPESTATUS[0]}"
echo
echo "### P5 modified table (emptied) + committed expected (r10 experiment shape; guard should fire)"
python3 - $T $W/scratch/table-emptied.json <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); d["entries"]=[]; d["quoted"]=[]
json.dump(d,open(sys.argv[2],"w"))
PY
python3 $P --root $REPO --rev HEAD --table $W/scratch/table-emptied.json --expected $E | tail -2
echo "P5 rc=${PIPESTATUS[0]}"
echo
echo "### P6 absent table"
python3 $P --root $REPO --rev HEAD --table $W/scratch/absent.json --expected $E | tail -2
echo "P6 rc=${PIPESTATUS[0]}"
echo
echo "### P7 foreign-CWD default-path invocation (no --table/--expected)"
( cd $W/scratch && python3 $P --root $REPO --rev HEAD ) | tail -2
echo "P7 rc=${PIPESTATUS[0]}"
echo
echo "### P8 flag surface"
python3 $P --help | sed -n '1,12p'
echo
echo "### P9 verdict-line-last with findings>0 (frozen rev, landed table)"
python3 $P --root $REPO --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table $T --expected $E | tail -1
echo "P9 rc=${PIPESTATUS[0]}"
echo
echo "### P10 tampered table at the default path in an isolated tree (fixture shape)"
rm -rf $W/isolated && mkdir -p $W/isolated && cp -r $G $W/isolated/citation-drift
python3 - $W/isolated/citation-drift/pointer-table.json <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p)); d["entries"]=[]; d["quoted"]=[]
json.dump(d,open(p,"w"))
PY
python3 $W/isolated/citation-drift/citation-drift-probe.py --root $REPO --rev HEAD | tail -2
echo "P10 rc=${PIPESTATUS[0]}"
} > $OUT 2>&1
echo "wrote $OUT"
