#!/bin/sh
# R41C2Shortcuts — exact rebuild of every number in the report.
# Runs from any cwd; writes only into the --out tree.
#   S=/fast/scratch/hyaku/kaidoku-r41/R41C2Shortcuts; mkdir -p "$S"; cd "$S"
#   export TMPDIR="$S"
#   A=<lane>/.ufo/waves/round-41/w1/artifacts/R41C2Shortcuts
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
A=${1:-$HERE}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin

# 1. exact-set grammar (the only grammar that exists at the base): every
#    candidate table is parsed by the frozen round-40 interpreter as a library.
python3 -I -B "$HERE/drv2.py" --out "$A"

# 2. proposed minimal v3 delta (superset cells `+a`): tables scored by the
#    local evaluator in drv3.py, features still from the frozen interpreter.
python3 -I -B "$HERE/drv3.py" --out "$A"

# 3. proof that the only shipped interpreter rejects a superset cell
python3 -I -B - "$A" <<'EOF'
import sys, os, importlib.util
a = sys.argv[1]
spec = importlib.util.spec_from_file_location('d', os.path.join(a, 'drv2.py'))
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
rows = [d.row('partial-body-failure', 'salvage-partial', gaps='+extractor-failure', files='>0')]
open(os.path.join(a, 'pluscell.md'), 'w').write(d.skill_doc(rows, d.ACTIONS))
EOF
python3 -I -B "$LANE/tools/round-40/sqfs-triage-v2.py" --skill "$A/pluscell.md" \
  "$LANE/corpus/evidence/round-40/c2/heldout/H01/envelope.json" || echo "exit=$? (expected 2)"

# 4. the best exact-grammar table through the real CLI on the committed envelopes
python3 -I -B "$LANE/tools/round-40/sqfs-triage-v2.py" --skill "$A/tables/T_min.md" \
  "$LANE"/corpus/evidence/round-40/c2/heldout/H{01,05,09,11,13,15,17,19,21,23,25}/envelope.json
