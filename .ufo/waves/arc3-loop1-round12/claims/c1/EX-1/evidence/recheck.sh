#!/usr/bin/env bash
set -euo pipefail

SEAT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE=/var/tmp/kaidoku-ex1-r12-analyze-function-id
REA=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
mkdir -p "$BASE/ghidra-tmp" "$BASE/alternate" "$SEAT/evidence/rerun"
cp "$SEAT/evidence/fixtures/primary/probe" "$BASE/probe"
cp "$SEAT/evidence/fixtures/alternate/probe" "$BASE/alternate/probe"

TMPDIR="$BASE/ghidra-tmp" node "$REA" function "$BASE/probe" probe_target --format json --full-output > "$SEAT/evidence/rerun/probe-base.json" 2> "$SEAT/evidence/rerun/probe-base.stderr"
TMPDIR="$BASE/ghidra-tmp" node "$REA" function "$BASE/alternate/probe" probe_target --format json --full-output > "$SEAT/evidence/rerun/probe-copy.json" 2> "$SEAT/evidence/rerun/probe-copy.stderr"
TMPDIR="$BASE/ghidra-tmp" node "$REA" function "$BASE/probe" probe_target --format json --full-output > "$SEAT/evidence/rerun/probe-base-repeat.json" 2> "$SEAT/evidence/rerun/probe-base-repeat.stderr"

for stderr in probe-base.stderr probe-copy.stderr probe-base-repeat.stderr; do
    test ! -s "$SEAT/evidence/rerun/$stderr"
done
python3 "$SEAT/evidence/recompute.py" "$SEAT/evidence/rerun"
