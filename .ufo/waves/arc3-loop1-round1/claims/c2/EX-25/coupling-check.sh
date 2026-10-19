#!/usr/bin/env bash
# EX-25 (c2, executor) post-implementation replay for EX-16's frozen-run guard.
# Read-only over the repo. All mutated inputs are scratch copies under this
# seat's claims dir; TMPDIR is redirected there because /tmp hit EDQUOT this
# wave. Never writes .ufo/gates/.
# usage: coupling-check.sh <label>
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
S=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-25
LABEL="${1:-after}"
OUT=$S/logs/$LABEL-coupling.txt
export TMPDIR=$S/scratch/tmp; mkdir -p "$TMPDIR" "$S/scratch" "$S/logs"
P=$G/citation-drift-probe.py; T=$G/pointer-table.json; E=$G/expected.json
probe() { python3 "$P" --root "$REPO" "$@"; }

{
echo "### EX-25 coupling-check label=$LABEL at $(date -Is)"
echo "### HEAD: $(git -C "$REPO" rev-parse HEAD)"
echo "### gate sha256 (worktree):"; sha256sum "$P" "$E" "$T"
echo

echo "### C0. landed guard identifiers (grep of the probe) ###"
grep -n "table_tampered\|pointer_table_tampered\|table_digest\|pointer_table_digest\|unpinned_table\|_tampered\|digest" "$P" | head -30
echo

echo "### C1. pinned digest in expected.json ###"
python3 - "$E" "$T" <<'PY'
import hashlib,json,sys
disk=hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()
e=json.load(open(sys.argv[1]))
flat={}
def walk(o,p=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,p+"/"+str(k))
    elif isinstance(o,str) and len(o)==64: flat[p]=o
walk(e)
print("on-disk pointer-table.json sha256:", disk)
for k,v in flat.items():
    if v==disk: print("PIN MATCHES DISK at key:", k)
print("all 64-hex strings in expected.json:", json.dumps(flat,indent=1))
print("selftest case list:", [c["case"] for c in e.get("selftest",[])])
print("selftest case_count:", len(e.get("selftest",[])))
PY
echo

echo "### R1. REQUIRED: probe at HEAD (probe semantics) ###"
probe --rev HEAD --table "$T" --expected "$E"; echo "exit=$?"; echo

echo "### R2. REQUIRED: probe --rev deadbeef ###"
probe --rev deadbeef --table "$T" --expected "$E"; echo "exit=$?"; echo

echo "### R3. REQUIRED: probe --strict at HEAD (gate map) ###"
probe --rev HEAD --table "$T" --expected "$E" --strict; echo "exit=$?"; echo

echo "### R4. REQUIRED: selftest ###"
probe --selftest --expected "$E"; echo "exit=$?"; echo

echo "### A1. ATTACK: semantic tamper via --table (valid JSON, never-matching must_match) ###"
python3 - "$T" "$S/scratch/table-tampered.json" <<'PY'
import json,sys
t=json.load(open(sys.argv[1]))
for e in t.get("entries",[]):
    if e.get("id")=="sc59-stanza-key-anchor":
        e["must_match"]="NEVER_MATCHES_THIS_STRING_ZZZ"; break
json.dump(t,open(sys.argv[2],"w"),indent=2)
PY
probe --rev HEAD --table "$S/scratch/table-tampered.json" --expected "$E"; echo "exit=$?"
echo "--- same, --strict ---"
probe --rev HEAD --table "$S/scratch/table-tampered.json" --expected "$E" --strict; echo "exit=$?"; echo

echo "### A2. ATTACK: emptied table (silent-findings class at HEAD) ###"
python3 - "$T" "$S/scratch/table-emptied.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); d["entries"]=[]; d["quoted"]=[]
json.dump(d,open(sys.argv[2],"w"))
PY
probe --rev HEAD --table "$S/scratch/table-emptied.json" --expected "$E"; echo "exit=$?"
echo "--- same, --strict ---"
probe --rev HEAD --table "$S/scratch/table-emptied.json" --expected "$E" --strict; echo "exit=$?"; echo

echo "### A3. ATTACK: absent table ###"
probe --rev HEAD --table "$S/scratch/no-such-table.json" --expected "$E"; echo "exit=$?"; echo

echo "### A4. ATTACK: unpinned expected.json (coupling point 3) ###"
python3 - "$E" "$S/scratch/expected-unpinned.json" <<'PY'
import json,sys
e=json.load(open(sys.argv[1]))
for k in list(e.keys()):
    if "table" in k.lower(): del e[k]
for k,v in list(e.items()):
    if isinstance(v,dict):
        for kk in list(v.keys()):
            if "pointer-table" in kk.lower() or "table_digest" in kk.lower(): del v[kk]
json.dump(e,open(sys.argv[2],"w"))
print("unpinned expected keys:", list(e.keys()))
PY
probe --rev HEAD --table "$T" --expected "$S/scratch/expected-unpinned.json"; echo "exit=$?"; echo

echo "### A5. ATTACK: guard vs rev-check ordering (deadbeef + tampered table) ###"
probe --rev deadbeef --table "$S/scratch/table-tampered.json" --expected "$E"; echo "exit=$?"; echo

echo "### A6. ATTACK: does the pin read the table at --rev or on disk? ###"
probe --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table "$T" --expected "$E" 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A7. ATTACK: formatting-only reindent of the table (byte-level pin?) ###"
python3 - "$T" "$S/scratch/table-reindented.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
json.dump(d,open(sys.argv[2],"w"),indent=4)   # same JSON, different bytes
PY
probe --rev HEAD --table "$S/scratch/table-reindented.json" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A8. ATTACK: table path that is a directory ###"
probe --rev HEAD --table "$S/scratch" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A9. ATTACK: expected.json absent ###"
probe --rev HEAD --table "$T" --expected "$S/scratch/no-such-expected.json" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A10. ATTACK: guard applied to a legitimate alternate table (fixture path) ###"
probe --rev HEAD --table "$S/scratch/table-tampered.json" --expected "$S/scratch/expected-unpinned.json" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### EX-25 coupling-check complete ###"
} > "$OUT" 2>&1
echo "wrote $OUT"
