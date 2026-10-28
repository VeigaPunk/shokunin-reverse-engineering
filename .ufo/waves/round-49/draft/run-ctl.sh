#!/usr/bin/env bash
# usage: run-ctl.sh <clone-from-mkclone.sh> <work-dir-under-/fast/scratch/hyaku/kaidoku-r49/<seat>/> [extra c1-controls.py args]
# Runs the C1 controls driver (CTL-C1-0..5 + POS) against the clone's dev freeze; prints one verdict line per control.
set -u
D=$1; W=$2; shift 2
export HYAKU_SCRATCH=/fast/scratch/hyaku
PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
rm -rf "$W/ctl-work" "$W/ctl-out"; mkdir -p "$W/ctl-work"
cd "$D" && python3 -I -B tools/round-49/c1-controls.py --root "$D" --freeze "$(git -C "$D" rev-parse HEAD)" \
  --counter "$D/tools/round-49/c1-counter.py" --pkg65 "$PKG" --work "$W/ctl-work" --out "$W/ctl-out" \
  --json-out "$W/ctl.json" --doc-dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts "$@" 2>&1 | tail -c 600
python3 - "$W/ctl.json" <<'P'
import json,sys
d=json.load(open(sys.argv[1]))
for k,v in d['controls'].items(): print(k,v['verdict'],v['exit_code'],v['why'][:160])
P
