#!/usr/bin/env bash
# RV-6 landing verification: run the moment EX-16's guard lands.
# Focus: exact string-set match between the code's guard-path finding ids and
# the registry row's declared ids; plus the pin value and the case tally.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
G=$REPO/.ufo/gates/citation-drift
cd "$REPO"

echo "### A. landed diff (gates dir)"
git diff --stat -- .ufo/gates/citation-drift/
git diff -- .ufo/gates/citation-drift/ | head -200

echo
echo "### B. post-state fingerprints"
sha256sum "$G"/* 2>/dev/null

echo
echo "### C. pin value vs actual table digest"
python3 - "$G/expected.json" "$G/pointer-table.json" <<'PY'
import hashlib,json,sys
exp=json.load(open(sys.argv[1]))
actual=hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()
print("expected.json keys:", list(exp.keys()))
found=[]
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+"/"+str(k))
    elif isinstance(o,str) and len(o)==64 and all(c in "0123456789abcdef" for c in o):
        found.append((path,o))
walk(exp)
print("64-hex strings in expected.json:")
for p,v in found: print("   %-40s %s %s" % (p,v,"<-- MATCHES table" if v==actual else ""))
print("actual sha256(pointer-table.json) =", actual)
PY

echo
echo "### D. finding ids present in the landed probe"
grep -n 'table_tampered\|pointer_table_unreadable\|unpinned\|snapshot_tampered\|table_unpinned\|pin' "$G/citation-drift-probe.py" | head -40

echo
echo "### E. CNE id list in the landed verdict()"
sed -n '/def verdict/,/return FAILED/p' "$G/citation-drift-probe.py"

echo
echo "### F. selftest + case table"
python3 "$G/citation-drift-probe.py" --selftest 2>&1 | tail -25
echo "selftest rc=${PIPESTATUS[0]}"
python3 - "$G/expected.json" <<'PY'
import json,sys
st=json.load(open(sys.argv[1])).get("selftest",[])
print("case_count=%d" % len(st))
for c in st: print("  %-22s exit=%s finding=%s" % (c.get("case"),c.get("exit_code"),c.get("finding")))
PY

echo
echo "### G. string-set comparison: row-declared ids vs code-emitted ids"
ROW=$S/patchtest/SKILL.md
if [ -f "$ROW" ]; then
  rowline=$(sed -n '371p' "$ROW")
  echo "-- ids named in the patched row --"
  echo "$rowline" | grep -o '`[a-z_]*`' | sort -u | tr '\n' ' '; echo
  echo "-- ids emitted by the landed code (guard paths) --"
  for id in table_tampered pointer_table_tampered pointer_table_unreadable unpinned_legacy table_unpinned; do
    if grep -q "\"$id\"" "$G/citation-drift-probe.py"; then echo "  EMITTED: $id"; fi
  done
else
  echo "patched row copy missing at $ROW"
fi

echo
echo "### H. clean run at HEAD with the landed guard"
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD 2>&1 | tail -2
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD --strict 2>&1 | tail -1

echo
echo "### I. full after-matrix"
bash "$S/after-harness.sh" 2>&1 | tail -80

echo
echo "### J. residual: fabricated (table, expected) pair pins itself"
printf '{"_doc":"rv6","entries":[],"quoted":[]}' > "$S/j-table.json"
python3 - "$S/j-table.json" "$S/j-expected.json" <<'PY'
import hashlib,json,sys
d=hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()
json.dump({"_doc":"rv6 fabricated pair","pointer_table":{"sha256":d},"snapshots":{}},open(sys.argv[2],"w"))
print("fabricated pin:",d)
PY
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD --table "$S/j-table.json" --expected "$S/j-expected.json" 2>&1 | tail -2
python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD --table "$S/j-table.json" --expected "$S/j-expected.json" >/dev/null 2>&1
echo "J rc=$? (rc=0 = residual confirmed: a fabricated pair reads clean)"
