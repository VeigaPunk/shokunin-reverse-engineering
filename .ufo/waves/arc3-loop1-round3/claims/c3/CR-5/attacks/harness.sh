#!/bin/bash
# CR-5 attack harness: run the COMMITTED probe against a scratch table.
# usage: harness.sh [TABLE] [REV] [ROOT]
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
WORK=/var/tmp/cr5-r3/attacks
GATE=$WORK/gate
TABLE=${1:-$WORK/cr5-candidates.json}
REV=${2:-HEAD}
ROOT=${3:-$REPO}
mkdir -p "$GATE"
cp "$REPO"/.ufo/gates/citation-drift/citation-drift-probe.py "$GATE"/
cp "$REPO"/.ufo/gates/citation-drift/expected.json "$GATE/expected-real.json"
python3 - "$TABLE" "$GATE/expected.json" <<'PY'
import hashlib, json, sys
table, outp = sys.argv[1], sys.argv[2]
exp = json.load(open("/var/tmp/cr5-r3/attacks/gate/expected-real.json"))
exp["pointer_table"]["sha256"] = hashlib.sha256(open(table, "rb").read()).hexdigest()
json.dump(exp, open(outp, "w"), indent=1)
PY
python3 "$GATE/citation-drift-probe.py" --root "$ROOT" --rev "$REV" \
  --table "$TABLE" --expected "$GATE/expected.json"
rc=$?
echo "HARNESS_EXIT=$rc"
exit $rc