#!/usr/bin/env bash
# usage: surv-one.sh <id>   builds a reflink clone of base, commits the mutated counter as its dev freeze, runs run-ctl.sh
set -u
id=$1; S=/fast/scratch/hyaku/kaidoku-r49/C1CounterMut; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku
D=$S/surv/$id; W=$S/surv-ctl/$id
rm -rf "$D" "$W"; mkdir -p "$S/surv" "$W"
cp -a --reflink=always "$S/base" "$D" || { echo "CLONE_FAIL"; exit 2; }
cp "$S/mut/$id/tools/round-49/c1-counter.py" "$D/tools/round-49/c1-counter.py.new" && mv "$D/tools/round-49/c1-counter.py.new" "$D/tools/round-49/c1-counter.py"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "TOPLEVEL_MISMATCH"; exit 2; }
git -C "$D" config user.name r49-dev; git -C "$D" config user.email r49@dev.invalid
git -C "$D" add tools/round-49/c1-counter.py && git -C "$D" commit -q -m "dev freeze: mutant $id"
echo "MUT_DEV_FREEZE=$(git -C "$D" rev-parse HEAD) counter_sha256=$(sha256sum "$D/tools/round-49/c1-counter.py" | cut -d' ' -f1)"
bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/run-ctl.sh "$D" "$W" > "$W/run-ctl.txt" 2>&1
echo "RUN_CTL_EXIT=$?"
