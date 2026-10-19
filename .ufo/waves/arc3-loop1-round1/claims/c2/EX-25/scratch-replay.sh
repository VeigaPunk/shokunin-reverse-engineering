#!/usr/bin/env bash
# EX-25 replay against the PL-2-plan-applied SCRATCH copy of the gate (EX-16's
# landing never arrived). The real .ufo/gates/ is untouched: G points at the
# scratch tree, and --root stays the real repo (read-only git objects).
# usage: scratch-replay.sh
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-25
G=$S/scratch/tree/.ufo/gates/citation-drift
export TMPDIR=$S/scratch/tmp; mkdir -p "$TMPDIR" "$S/logs"
P=$G/citation-drift-probe.py; T=$G/pointer-table.json; E=$G/expected.json
OUT=$S/logs/after-planapplied-coupling.txt
probe() { python3 "$P" --root "$REPO" "$@"; }

{
echo "### EX-25 scratch replay (PL-2 plan applied) at $(date -Is)"
echo "### real HEAD: $(git -C "$REPO" rev-parse HEAD)"
echo "### scratch gate sha256:"; sha256sum "$P" "$E" "$T"
echo "### real gate sha256 (must be unchanged):"
sha256sum "$REPO/.ufo/gates/citation-drift/citation-drift-probe.py" \
         "$REPO/.ufo/gates/citation-drift/expected.json" \
         "$REPO/.ufo/gates/citation-drift/pointer-table.json"
echo

echo "### C0. landed guard identifiers (grep of the patched probe) ###"
grep -n "pointer_table_tampered\|pointer_table_unpinned\|pointer_table\b\|pin = \|table_bytes" "$P" | head -25
echo

echo "### C1. pinned digest in expected.json vs on-disk table ###"
python3 - "$E" "$T" <<'PY'
import hashlib,json,sys
disk=hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()
e=json.load(open(sys.argv[1]))
pin=e.get("pointer_table",{}).get("sha256")
print("on-disk (scratch) pointer-table.json sha256:", disk)
print("pinned:", pin)
print("MATCH" if pin==disk else "MISMATCH")
print("selftest case_count:", len(e.get("selftest",[])))
print("selftest cases:", [c["case"] for c in e.get("selftest",[])])
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

echo "### A1. semantic tamper via --table (never-matching must_match) ###"
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

echo "### A2. emptied table (fully silent at HEAD) ###"
python3 - "$T" "$S/scratch/table-emptied.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); d["entries"]=[]; d["quoted"]=[]
json.dump(d,open(sys.argv[2],"w"))
PY
probe --rev HEAD --table "$S/scratch/table-emptied.json" --expected "$E"; echo "exit=$?"
echo "--- same, --strict ---"
probe --rev HEAD --table "$S/scratch/table-emptied.json" --expected "$E" --strict; echo "exit=$?"; echo

echo "### A3. absent table ###"
probe --rev HEAD --table "$S/scratch/no-such-table.json" --expected "$E"; echo "exit=$?"; echo

echo "### A4. unpinned expected.json (real pre-EX-16 expected) ###"
probe --rev HEAD --table "$T" --expected "$REPO/.ufo/gates/citation-drift/expected.json"; echo "exit=$?"; echo

echo "### A5. guard vs rev-check ordering (deadbeef + tampered table) ###"
probe --rev deadbeef --table "$S/scratch/table-tampered.json" --expected "$E"; echo "exit=$?"; echo

echo "### A6. old rev with pinned table (frozen_run.revision) ###"
probe --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table "$T" --expected "$E" 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A7. formatting-only reindent (byte-level pin) ###"
python3 - "$T" "$S/scratch/table-reindented.json" <<'PY'
import json,sys
json.dump(json.load(open(sys.argv[1])),open(sys.argv[2],"w"),indent=4)
PY
probe --rev HEAD --table "$S/scratch/table-reindented.json" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A8. table path is a directory ###"
probe --rev HEAD --table "$S/scratch" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A9. expected.json absent ###"
probe --rev HEAD --table "$T" --expected "$S/scratch/no-such-expected.json" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A10. alternate table + pinned expected (path-scoped bypass?) ###"
probe --rev HEAD --table "$S/scratch/table-tampered.json" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A11. table that is not valid JSON but matches no pin ###"
printf '{ not json' > "$S/scratch/table-notjson.json"
probe --rev HEAD --table "$S/scratch/table-notjson.json" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### A12. byte-identical copy of the table at another path (guard path-scoped?) ###"
cp "$T" "$S/scratch/table-copy-same-bytes.json"
probe --rev HEAD --table "$S/scratch/table-copy-same-bytes.json" --expected "$E" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"; echo

echo "### EX-25 scratch replay complete ###"
} > "$OUT" 2>&1
echo "wrote $OUT"
