#!/usr/bin/env bash
# VZ-2 independent convergence harness for the citation-drift frozen-run guard.
# Usage: attack.sh <gate-dir> <repo> <outdir> <label>
# Read-only over the repo; all mutated inputs are scratch copies.
set -u
G=$1; REPO=$2; OUT=$3; LABEL=$4
mkdir -p "$OUT"
P=$G/citation-drift-probe.py
E=$G/expected.json

run() { # run <label> <table> [extra args...]
  local label=$1 table=$2; shift 2
  local out rc
  out=$(python3 "$P" --root "$REPO" --rev HEAD --table "$table" --expected "$E" "$@" 2>&1)
  rc=$?
  echo "[$LABEL/$label] rc=$rc | $(echo "$out" | tail -1)"
  echo "$out" >> "$OUT/$label.out"
}

# fresh scratch dir for this family
S=$OUT/fixtures; rm -rf "$S"; mkdir -p "$S"

# 1. absent table
run "absent" "$S/does-not-exist.json"

# 2. tampered: valid JSON, entries emptied
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$S/t-empty.json"
run "emptied" "$S/t-empty.json"

# 3. tampered: {} no keys
printf '{}' > "$S/t-brace.json"
run "brace" "$S/t-brace.json"

# 4. tampered: one byte flipped in the real table (copy)
cp "$G/pointer-table.json" "$S/t-flip.json"
python3 - "$S/t-flip.json" <<'PY'
import sys
p=sys.argv[1]; d=open(p,'rb').read()
i=d.find(b'pointer-table')
d=d[:5]+bytes([d[5]^1])+d[6:] if d[5:6] not in (b' ',) else d
open(p,'wb').write(d)
PY
run "byteflip" "$S/t-flip.json"

# 5. tampered: whitespace-only reformat of the real table (same semantics)
python3 - "$G/pointer-table.json" "$S/t-reformat.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
open(sys.argv[2],'w').write(json.dumps(d,indent=1))
PY
run "reformat" "$S/t-reformat.json"

# 6. tampered: must_match weakened to .* on the real table
python3 - "$G/pointer-table.json" "$S/t-weaken.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for e in d.get("entries",[]): e["must_match"]=".*"
for q in d.get("quoted",[]): q["must_match"]=".*"
json.dump(d,open(sys.argv[2],"w"))
PY
run "weakened" "$S/t-weaken.json"

# 7. table path is a directory
mkdir -p "$S/dirtable"; run "dir" "$S/dirtable"

# 8. clean control: the real table from this gate dir
run "clean" "$G/pointer-table.json"
run "clean-strict" "$G/pointer-table.json" --strict

# 9. selftest of this gate dir
python3 "$P" --selftest --expected "$E" > "$OUT/selftest.out" 2>&1
echo "[$LABEL/selftest] rc=$? | $(tail -1 "$OUT/selftest.out")"

# 10. digest pin consistency: expected.json pin vs actual table sha256
python3 - "$G/expected.json" "$G/pointer-table.json" <<'PY' | tee "$OUT/pin-check.out"
import hashlib,json,sys
exp=json.load(open(sys.argv[1])); tab=open(sys.argv[2],'rb').read()
dig=hashlib.sha256(tab).hexdigest()
pin=None
for k in ("pointer_table_sha256","table_sha256","pointer-table.json"):
    v=exp.get(k)
    if isinstance(v,str): pin=v
snap=(exp.get("snapshots") or {}).get("pointer-table.json")
if snap: pin=snap
print("actual_table_sha256=%s" % dig)
print("pinned=%s" % (pin or "<NONE>"))
print("pin_ok=%s" % ("yes" if pin==dig else "no"))
PY
echo "[$LABEL/pin] $(tail -1 "$OUT/pin-check.out")"
