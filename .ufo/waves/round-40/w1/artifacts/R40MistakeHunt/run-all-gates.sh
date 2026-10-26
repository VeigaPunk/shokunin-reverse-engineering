#!/bin/sh
# Run every red and green case of the R40MistakeHunt gates into runs.txt.
# Usage: LANE=/path/to/kaidoku-shokunin sh run-all-gates.sh > runs.txt 2>&1
set -u
A=$(cd "$(dirname "$0")" && pwd)
L=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
S=${TMPDIR:-/tmp}
: "${TMPDIR:=$S}"
export TMPDIR
G="$S/mistake-green"
FREEZE39=8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b

run() { echo "\$ $*"; "$@"; echo "exit=$?"; echo; }

cd "$L" || exit 2
echo "### host: $(uname -srm) | python3 $(python3 -V 2>&1 | cut -d' ' -f2) | lane HEAD $(git rev-parse --short HEAD)"
echo

echo "=== MH-1 control inputs: (a) tables under the controls dir, (b) the freeze's registered tables ==="
run python3 -I -B "$A/control-freeze-gate.py" --root "$L" --freeze "$FREEZE39" \
    --tables .ufo/waves/round-39/controls/tables \
    --interpreter tools/round-39/sqfs-triage.py --work "$S"
run python3 -I -B "$A/control-freeze-gate.py" --root "$L" --freeze "$FREEZE39" \
    --tables .ufo/waves/round-39/w1/artifacts/R39C2Shortcuts \
    --interpreter tools/round-39/sqfs-triage.py --work "$S"

echo "=== MH-2 score receipts: exit code + ledger status ==="
run python3 -I -B "$A/receipt-fields-gate.py" --scores .ufo/waves/round-39/l1/scores \
    --ledgers .ufo/waves/round-39/r39-w1-results.json .ufo/waves/round-39/r39-w2-results.json

echo "=== MH-3 report minimum content ==="
run python3 -I -B "$A/report-content-gate.py" \
    --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kaidoku.md

echo "=== MH-4 depth instrument headroom ==="
run python3 -I -B "$A/depth-delta-gate.py" --root "$L" \
    --base a2f64e1da78afcf8cc39287106604dbcc270844c --tip 52b0eb2907c704ed5f184c47b14c723208e5cbbc
run python3 -I -B "$A/depth-delta-gate.py" --root "$L" \
    --base fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f --tip fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f

echo "=== MH-5 writer mode named for a layout it does not emit ==="
run python3 -I -B "$A/avm-mode-gate.py" --gen tools/round-39/gen-squashfs.py --work "$S"
run python3 -I -B "$A/avm-mode-gate.py" --gen "$A/gen-squashfs-avm-mode-fixed.py" --work "$S"

echo "=== MH-6 v1 AVM rows keyed on the marker ==="
run python3 -I -B "$A/avm-row-guard.py" --table SKILL.md
run python3 -I -B "$A/avm-row-guard.py" --table "$A/table-v2-proposed.md"

echo "=== MH-7 domain guard (R39-CL1) ==="
run python3 -I -B "$A/check-domain-guard.py" --table SKILL.md \
    --envelope corpus/evidence/round-27/c1/envelopes/jq-function-base.json \
    --envelope corpus/evidence/round-26/c1/envelopes/function-base.json
run python3 -I -B "$A/check-domain-guard.py" --table "$A/table-v2-proposed.md" \
    --envelope corpus/evidence/round-27/c1/envelopes/jq-function-base.json \
    --envelope corpus/evidence/round-26/c1/envelopes/function-base.json

echo "=== MH-8 mixed symlinks (R39-CL2) ==="
run python3 -I -B "$A/check-mixed-symlinks.py" --table SKILL.md \
    --envelope corpus/evidence/round-39/c1/K5/after.json \
    --envelope corpus/evidence/round-39/c1/K6/after.json
run python3 -I -B "$A/check-mixed-symlinks.py" --table "$A/table-v2-proposed.md" \
    --envelope corpus/evidence/round-39/c1/K5/after.json \
    --envelope corpus/evidence/round-39/c1/K6/after.json

echo "=== MH-9 label-only scoring (R39-CL3) ==="
run python3 -I -B "$A/action-scoring-check.py" --root "$L" --work "$S"

echo "=== MH-10 the interpreter's embedded table is a second copy of the shipped rule ==="
run python3 -I -B "$A/table-copies-gate.py" --interpreter tools/round-39/sqfs-triage.py \
    --skill SKILL.md --heldout corpus/evidence/round-39/c2/heldout --work "$S" \
    --fix-out "$S/sqfs-triage-single-source.py"
run python3 -I -B "$A/table-copies-gate.py" --interpreter "$S/sqfs-triage-single-source.py" \
    --skill SKILL.md --heldout corpus/evidence/round-39/c2/heldout --work "$S"

echo "=== MH-11 the living axis row lags the landing commit ==="
run python3 -I -B "$A/axis-record-gate.py" --root "$L" \
    --rev 6fdaf4f162aff156fcef0e52998a5469c64fd6f0
run python3 -I -B "$A/axis-record-gate.py" --root "$L" \
    --rev 2b0b6a29578c0b8917f677321557d96a444e994e

echo "=== MH-12 committed provenance argv must name the command that ran ==="
run python3 -I -B "$A/evidence-argv-gate.py" --heldout corpus/evidence/round-39/c2/heldout \
    --fix-out "$S/fixed-run"
run python3 -I -B "$A/evidence-argv-gate.py" --heldout "$S/fixed-run"

echo "=== draft D6: a v2-shaped table under the frozen interpreter ==="
run python3 -I -B tools/round-39/sqfs-triage.py --skill "$A/table-v2-proposed.md" --table-only

echo "=== green fixtures (built from lane files; nothing in the lane is written) ==="
run python3 -I -B "$A/green-fixtures.py" --work "$G"
CF=$(python3 -c "import json;print(json.load(open('$G/fixtures.json'))['ctrlrepo_freeze'])")
CB=$(python3 -c "import json;print(json.load(open('$G/fixtures.json'))['ctrlrepo_bad_freeze'])")
DB=$(python3 -c "import json;print(json.load(open('$G/fixtures.json'))['depthrepo_base'])")
DT=$(python3 -c "import json;print(json.load(open('$G/fixtures.json'))['depthrepo_tip'])")

echo "--- MH-1 green: table committed in the freeze commit ---"
run python3 -I -B "$A/control-freeze-gate.py" --root "$G/ctrlrepo" --freeze "$CF" \
    --tables controls/tables --interpreter "$L/tools/round-39/sqfs-triage.py" --work "$S"
echo "--- MH-1 red half: malformed table frozen ---"
run python3 -I -B "$A/control-freeze-gate.py" --root "$G/ctrlrepo-bad" --freeze "$CB" \
    --tables controls/tables --interpreter "$L/tools/round-39/sqfs-triage.py" --work "$S"
echo "--- MH-2 green ---"
run python3 -I -B "$A/receipt-fields-gate.py" --scores "$G/scores" \
    --ledgers "$G/ledgers/r39-w1-results.json" "$G/ledgers/r39-w2-results.json"
echo "--- MH-3 green ---"
run python3 -I -B "$A/report-content-gate.py" --report "$G/report.md"
echo "--- MH-4 green: base has headroom ---"
run python3 -I -B "$A/depth-delta-gate.py" --root "$G/depthrepo" --base "$DB" --tip "$DT"
echo
echo "### end"
