#!/usr/bin/env bash
# SC-4: independent measurement of EX-21's guard prototype (reference
# implementation candidate for EX-16's real-target landing).
# Read-only over the real gate: the prototype is a copy; all mutated inputs are
# scratch copies under this artifact dir. TMPDIR redirected here (/tmp quota).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
S=$(cd "$(dirname "$0")" && pwd)
EX21=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-21/tmp/proto
EX21ROOT=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-21
OUT=$S/verify-proto.txt
export TMPDIR=$S/scratch/tmp
mkdir -p "$TMPDIR" "$S/scratch/proto"
P=$S/scratch/proto/probe.py
cp "$EX21/probe.py" "$P"

# pinned expected.json = the real one + the pin of the real table digest
python3 - "$G/expected.json" "$G/pointer-table.json" "$S/scratch/expected-pinned.json" <<'PY'
import hashlib,json,sys
e=json.load(open(sys.argv[1]))
e["table_sha256"]=hashlib.sha256(open(sys.argv[2],"rb").read()).hexdigest()
json.dump(e,open(sys.argv[3],"w"))
print("Pinned digest written:", e["table_sha256"])
PY

run() { # run <label> <expected probe rc> <args...>
  local label=$1 want=$2; shift 2
  local out rc
  out=$(python3 "$P" --root "$REPO" --rev HEAD "$@" 2>&1); rc=$?
  echo "### $label (want rc=$want, got rc=$rc)"
  echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -2
  echo
}

{
echo "### SC-4 verify-proto at $(date -Is)"
echo "### proto source: $EX21/probe.py"
sha256sum "$EX21/probe.py" "$EX21/expected.json"
echo
run "P1 proto + real table + pinned expected" 0 \
  --table "$G/pointer-table.json" --expected "$S/scratch/expected-pinned.json"
run "P2 proto + weakened table + pinned expected" 2 \
  --table "$S/scratch/table-weakened.json" --expected "$S/scratch/expected-pinned.json"
run "P3 proto + emptied table + pinned expected --strict" 2 --strict \
  --table "$S/scratch/table-emptied.json" --expected "$S/scratch/expected-pinned.json"
run "P4 ATTACK: weakened table + UNPINNED expected (pin field deleted)" 0 \
  --table "$S/scratch/table-weakened.json" --expected "$S/scratch/expected-unpinned.json"
echo "^ rc=0 here means the one-field deletion defeats the guard (skip-on-unpinned)"
echo
run "P5 proto + absent table + pinned expected" 2 \
  --table "$S/scratch/does-not-exist.json" --expected "$S/scratch/expected-pinned.json"
echo "### P6 proto selftest (want 13/13 exit 0)"
out=$(python3 "$P" --selftest --expected "$EX21/expected.json" 2>&1); rc=$?
echo "$out" | tail -1
echo "rc=$rc"
echo

echo "### P7 does EX-21's published proto-probe.diff reproduce EX-21's probe.py?"
mkdir -p "$S/scratch/proto-apply"
cd "$S/scratch/proto-apply"
git -C "$REPO" show HEAD:.ufo/gates/citation-drift/citation-drift-probe.py > citation-drift-probe.py
python3 - "$EX21ROOT/logs/proto-probe.diff" rewritten.diff <<'PY'
import sys
lines=open(sys.argv[1]).read().split("\n")
out=[]
for l in lines:
    if l.startswith("--- "): l="--- citation-drift-probe.py"
    elif l.startswith("+++ "): l="+++ citation-drift-probe.py"
    out.append(l)
open(sys.argv[2],"w").write("\n".join(out))
PY
patch -p0 --dry-run < rewritten.diff >/dev/null; echo "dry-run rc=$?"
patch -p0 < rewritten.diff >/dev/null; echo "apply rc=$?"
echo "applied sha256: $(sha256sum citation-drift-probe.py | cut -d' ' -f1)"
echo "EX-21 probe.py: $(sha256sum "$EX21/probe.py" | cut -d' ' -f1)"
echo "delta (applied vs EX-21 probe.py):"
diff -u citation-drift-probe.py "$EX21/probe.py" | sed -n '1,14p'
echo
echo "### P7b selftest of the diff-applied probe (want 13/13)"
out=$(python3 citation-drift-probe.py --selftest --expected "$EX21/expected.json" 2>&1); rc=$?
echo "$out" | grep -c "SELFTEST_CASE: FAILED" | sed 's/^/FAILED_cases=/'
echo "$out" | tail -1
echo "rc=$rc"
cd "$S"
} > "$OUT" 2>&1
echo "wrote $OUT"
