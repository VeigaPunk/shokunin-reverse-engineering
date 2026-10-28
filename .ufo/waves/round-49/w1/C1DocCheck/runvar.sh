#!/usr/bin/env bash
# usage: runvar.sh <script> <tag> <docdir>
S=/fast/scratch/hyaku/kaidoku-r49/C1DocCheck; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku
D=$S/clone; W=$S/w-$2; PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
rm -rf $W; mkdir -p $W/ctl-work; cd $D
python3 -I -B $1 --root $D --freeze "$(git -C $D rev-parse HEAD)" --counter $D/tools/round-49/c1-counter.py --pkg65 $PKG --work $W/ctl-work --out $W/ctl-out --json-out $W/ctl.json --doc-dir $3 --controls pos > $W/run.out 2>&1
echo "$2 exit=$?"
