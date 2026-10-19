#!/usr/bin/env bash
# SC-4 scribe harness: pre/post measurement for the c2 citation-drift guard
# changeset. Read-only over the real target; every mutated input is a scratch
# copy under this artifact dir. TMPDIR is redirected here because /tmp hit the
# user quota this wave (RV-6 precedent).
# Usage: verify-changeset.sh <label>   -> writes verify-<label>.txt
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
S=$(cd "$(dirname "$0")" && pwd)
LABEL=${1:-unlabeled}
OUT=$S/verify-$LABEL.txt
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR" "$S/scratch"

{
echo "### SC-4 verify-changeset label=$LABEL at $(date -Is)"
echo "### HEAD: $(git -C "$REPO" rev-parse HEAD)"
echo "### sha256 (worktree):"
sha256sum "$G"/citation-drift-probe.py "$G"/expected.json "$G"/pointer-table.json
echo

echo "### 1. selftest (full case list)"
python3 "$G/citation-drift-probe.py" --selftest 2>&1
echo "selftest rc=$?"
echo

echo "### 1b. committed selftest case table (expected.json)"
python3 - "$G/expected.json" <<'PY'
import json,sys
e=json.load(open(sys.argv[1]))
for c in e.get("selftest",[]):
    print("CASE %-18s exit=%s finding=%s" % (c["case"], c["exit_code"], c["finding"]))
print("case_count=%d" % len(e.get("selftest",[])))
PY
echo

echo "### 2. probe at HEAD (probe semantics)"
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$G/pointer-table.json" --expected "$G/expected.json" 2>&1 | tail -2
echo

echo "### 3. probe at HEAD (--strict)"
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD --strict \
  --table "$G/pointer-table.json" --expected "$G/expected.json" 2>&1 | tail -2
echo

echo "### 4. guard attack: valid-JSON semantic tamper passed via --table"
python3 - "$G/pointer-table.json" "$S/scratch/table-emptied.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
d["entries"]=[]
d["quoted"]=[]
json.dump(d,open(sys.argv[2],"w"))
PY
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$S/scratch/table-emptied.json" --expected "$G/expected.json" 2>&1)
echo "rc=$?"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 5. guard attack: weakened must_match table passed via --table"
python3 - "$G/pointer-table.json" "$S/scratch/table-weakened.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for e in d.get("entries",[]): e["must_match"]=".*"
for q in d.get("quoted",[]): q["must_match"]=".*"
json.dump(d,open(sys.argv[2],"w"))
PY
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$S/scratch/table-weakened.json" --expected "$G/expected.json" 2>&1)
echo "rc=$?"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 6. absent table path"
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$S/scratch/does-not-exist.json" --expected "$G/expected.json" 2>&1)
echo "rc=$?"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 7. pinned-digest consistency (if expected.json pins the table)"
python3 - "$G/expected.json" "$G/pointer-table.json" <<'PY'
import hashlib,json,sys
exp=json.load(open(sys.argv[1])); actual=hashlib.sha256(open(sys.argv[2],"rb").read()).hexdigest()
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,str) and len(v)==64 and all(c in "0123456789abcdef" for c in v):
                print("PINNED %s%s = %s" % (path,k,v))
            walk(v,path+k+".")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+"[%d]."%i)
walk(exp)
print("ACTUAL sha256(pointer-table.json) = %s" % actual)
PY
echo

echo "### 8. guard attack: unpinned expected.json (pin field deleted) with the REAL table"
python3 - "$G/expected.json" "$S/scratch/expected-unpinned.json" <<'PY'
import json,sys
e=json.load(open(sys.argv[1]))
for k in list(e.keys()):
    if "table" in k.lower(): del e[k]
json.dump(e,open(sys.argv[2],"w"))
print("keys after deletion:", sorted(e.keys()))
PY
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$G/pointer-table.json" --expected "$S/scratch/expected-unpinned.json" 2>&1)
echo "rc=$?"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 9. tampered-table run must carry exactly one finding (no entry evaluation)"
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$S/scratch/table-emptied.json" --expected "$G/expected.json" 2>&1)
echo "finding_lines=$(echo "$out" | grep -c '^CITATION_DRIFT: ')"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 10. default-path invocation (no --table/--expected) from a foreign CWD"
out=$(cd "$S/scratch" && python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD 2>&1)
echo "rc=$?"
echo "$out" | grep -E "^CITATION_DRIFT_TABLE|^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -3
echo

echo "### 11. residual limit: forged --expected (pin recomputed for a tampered table)"
python3 - "$G/expected.json" "$S/scratch/table-emptied.json" "$S/scratch/expected-forged.json" <<'PY'
import hashlib,json,sys
e=json.load(open(sys.argv[1]))
p=e.get("pointer_table")
if isinstance(p, dict) and "sha256" in p:
    p["sha256"]=hashlib.sha256(open(sys.argv[2],"rb").read()).hexdigest()
else:
    e["pointer_table"]={"sha256": hashlib.sha256(open(sys.argv[2],"rb").read()).hexdigest()}
json.dump(e,open(sys.argv[3],"w"))
PY
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD \
  --table "$S/scratch/table-emptied.json" --expected "$S/scratch/expected-forged.json" 2>&1)
echo "rc=$? (rc=0 = the caller who forges --expected still reads clean; inherent limit)"
echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -2
} > "$OUT" 2>&1
echo "wrote $OUT"
