#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kaidoku-r49/ConnSeparability; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku
PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
X=$S/ctlX/ctl-work/run.oosncacy/sandbox-pos; Y=$S/Y
FREEZE=$(git -C $Y rev-parse 352e24c6728df9da4b7aa2e410cfbc4ab4a70622^{commit})
XREV=$(git -C $X rev-parse HEAD); YREV=$(git -C $Y rev-parse HEAD)
echo "FREEZE=$FREEZE XREV=$XREV YREV=$YREV" > $S/out/revs.txt
run() { # tag script root rev extra...
  local tag=$1 scr=$2 root=$3 rev=$4; shift 4
  mkdir -p $S/work/$tag
  TRACE_LOG=$S/trace/$tag.log PATH=$S/shim:$PATH python3 -I -B "$scr" --root "$root" --rev "$rev" --freeze "$FREEZE" "$@" > $S/out/$tag.stdout 2> $S/out/$tag.stderr
  echo "$? " > $S/out/$tag.exit
}
C1=$X/tools/round-49/c1-counter.py; C2=$X/tools/round-49/c2-mismatch.py
run c1-X  $C1 $X $XREV --pkg65 $PKG --work $S/work/c1-X --json-out $S/out/c1-X.json &
run c1-Y  $C1 $Y $YREV --pkg65 $PKG --work $S/work/c1-Y --json-out $S/out/c1-Y.json &
run c1-F  $C1 $Y $FREEZE --pkg65 $PKG --work $S/work/c1-F --json-out $S/out/c1-F.json &
run c2-X  $C2 $X $XREV --battery --json-out $S/out/c2-X.json &
run c2-Y  $C2 $Y $YREV --battery --json-out $S/out/c2-Y.json &
run c2-F  $C2 $Y $FREEZE --json-out $S/out/c2-F.json &
wait
echo done
