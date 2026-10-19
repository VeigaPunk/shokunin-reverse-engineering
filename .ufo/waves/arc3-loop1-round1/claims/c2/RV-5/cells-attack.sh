#!/usr/bin/env bash
# RV-5 attacks: the guard's scope limits, measured against any staged gate dir.
# Usage: cells-attack.sh <gate-dir> <label-prefix>
#   A1 co-mutation: tampered table + the pin recomputed to match it
#      (the pair is rewritten in one edit; no verdict change is expected)
#   A2 reformat: byte-different, semantically identical table (json re-dump)
#      (byte-exactness cost: a harmless reformat must read as CNE, never silent)
set -u
S=$(cd "$(dirname "$0")" && pwd)
. "$S/mutation-harness.sh"
GATEDIR=$1; PF=$2
P=$GATEDIR/probe.py; E=$GATEDIR/expected.json; T=$GATEDIR/pointer-table.json
python3 - "$E" "$T" "$S/fixtures/table-emptied.json" "$S/fixtures" <<'PY'
import hashlib, json, sys
exp_path, table_path, emptied_path, out = sys.argv[1:5]
raw = open(table_path, "rb").read()
emp = open(emptied_path, "rb").read()
exp = json.load(open(exp_path))
def scrub(o, dig):
    if isinstance(o, dict):
        return {k: (dig if v == hashlib.sha256(raw).hexdigest() else scrub(v, dig)) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub(v, dig) for v in o]
    return o
forged = scrub(exp, hashlib.sha256(emp).hexdigest())
open(out + "/expected-forged-pin.json", "w").write(json.dumps(forged))
reformatted = json.dumps(json.loads(raw)).encode()
open(out + "/table-reformatted.json", "wb").write(reformatted)
print("A-fixtures: emptied=%s reformatted=%s pin-in-forged=%s"
      % (hashlib.sha256(emp).hexdigest()[:16], hashlib.sha256(reformatted).hexdigest()[:16],
         hashlib.sha256(emp).hexdigest()[:16]))
PY
echo "### $PF attacks (probe=$(sha256sum "$P" | cut -c1-16) exp=$(sha256sum "$E" | cut -c1-16))"
run $PF-A1-comutation "$P" "$S/fixtures/expected-forged-pin.json" "$S/fixtures/table-emptied.json"
run $PF-A1-comutation-strict "$P" "$S/fixtures/expected-forged-pin.json" "$S/fixtures/table-emptied.json" --strict
run $PF-A2-reformat "$P" "$E" "$S/fixtures/table-reformatted.json"
run $PF-A2-reformat-strict "$P" "$E" "$S/fixtures/table-reformatted.json" --strict
