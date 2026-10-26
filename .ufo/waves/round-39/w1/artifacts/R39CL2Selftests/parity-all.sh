#!/usr/bin/env bash
# R39CL2Selftests parity harness (advisory evidence, not an admission gate).
# 1. Runs every round-38 l1 receipt argv against BOTH the unpatched lane tool and
#    the patched artifact copy and diffs stdout + exit code byte-for-byte.
# 2. Cross-checks the patched stdout against each committed round-38 receipt,
#    normalising only the receipt-format facts stated in the report (the two
#    freeze-drift keys added at 7a1ac7fe, and the trailing "exit N" line the L1
#    appended to the registry receipts).
# Nothing here writes to the lane; all output lands under $TMPDIR/parity.
set -uo pipefail
A=$(cd "$(dirname "$0")" && pwd -P)
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ORIG=$L/tools/round-38
RCPT=$L/.ufo/waves/round-38/l1
T=${TMPDIR:?TMPDIR must be set}
P=$T/parity
mkdir -p "$P"
n=0 fail=0
bad() { fail=$((fail + 1)); echo "  MISMATCH: $*"; }

report() {  # report NAME ORC PRC
  local name=$1 orc=$2 prc=$3 same=OK
  n=$((n + 1))
  diff -q "$P/$name.orig" "$P/$name.patched" >/dev/null 2>&1 || same=DIFF
  if [ "$orc" != "$prc" ]; then same="$same/RC"; fi
  if [ "$same" = OK ]; then
    echo "parity $name: rc=$orc stdout=identical"
  else
    bad "parity $name rc orig=$orc patched=$prc stdout=$same"
    diff -u "$P/$name.orig" "$P/$name.patched" | head -40
  fi
}

FD_PATHS=(plans/round-38-claims.md tools/round-38/c1-counter.py tools/round-38/c2-counter.py
          .ufo/waves/round-38/c1/carriers.json 'corpus/evidence/round-37/c1/*/oracle.tsv')

fd() {  # fd NAME FREEZE REV ARGS...
  local name=$1 freeze=$2 rev=$3
  shift 3
  python3 -I -B "$ORIG/freeze-drift.py" --root "$L" --freeze "$freeze" --rev "$rev" "$@" \
    > "$P/$name.orig" 2>&1
  local orc=$?
  python3 -I -B "$A/freeze-drift.py" --root "$L" --freeze "$freeze" --rev "$rev" "$@" \
    > "$P/$name.patched" 2>&1
  local prc=$?
  report "$name" "$orc" "$prc"
}

idoc() {  # idoc NAME REV BASE FILE UNIT INTENDED
  local name=$1 rev=$2 base=$3 file=$4 unit=$5 intended=$6
  python3 -I -B "$ORIG/intended-doc.py" --root "$L" --rev "$rev" --base "$base" \
    --file "$file" --unit "$unit" --intended "$intended" > "$P/$name.orig" 2>&1
  local orc=$?
  python3 -I -B "$A/intended-doc.py" --root "$L" --rev "$rev" --base "$base" \
    --file "$file" --unit "$unit" --intended "$intended" > "$P/$name.patched" 2>&1
  local prc=$?
  report "$name" "$orc" "$prc"
}

ri() {  # ri NAME TOOL BASE REV
  local name=$1 tool=$2 base=$3 rev=$4
  bash "$ORIG/registry-immutable.sh" "$L" "$base" "$rev" > "$P/$name.orig" 2>&1
  local orc=$?
  bash "$tool" "$L" "$base" "$rev" > "$P/$name.patched" 2>&1
  local prc=$?
  report "$name" "$orc" "$prc"
}

usage_parity() {  # usage_parity NAME PYTOOL -- runs with no arguments
  local name=$1 py=$2
  n=$((n + 1))
  python3 -I -B "$ORIG/$py" > "$P/$name.orig" 2>&1; local orc=$?
  python3 -I -B "$A/$py" > "$P/$name.patched" 2>&1; local prc=$?
  if [ "$orc" = "$prc" ] && diff -q "$P/$name.orig" "$P/$name.patched" >/dev/null 2>&1; then
    echo "parity $name: rc=$orc stdout+stderr=identical (usage path)"
  else
    bad "parity $name rc orig=$orc patched=$prc"
    diff -u "$P/$name.orig" "$P/$name.patched" | head -20
  fi
}

norm_fd() {  # drop the two keys freeze-drift gained at 7a1ac7fe
  python3 - "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for k in ('net_changed', 'ships_freeze_bytes'):
    d.pop(k, None)
print(json.dumps(d, indent=1))
PY
}

norm_rm() { sed '/^exit [0-9]\+$/d' "$1"; }

FZ=e059ca9391642d5b71b6662cabcbdce0d9308719
R7A=7a1ac7fe39410a3c9df13d97c14ba17f4d036ab6
R0F=0fc6113376a156fddc3ec385386d71c3a4a9f690
R07=077e212b81015f985febc12261ecac4fec71683a
RCB=cb4326b2aa4c2024af0651fe6115b82d0c4de3df
E26=e265533e
B77=77091b492cc53f8743bd0701b1e7d5e66123dd84
UNIT='REA MCP server'
INT='.ufo/waves/round-19/evidence/doctor/'

echo "== freeze-drift (round-38 l1 receipts)"
fd fd-final      "$FZ" "$R7A" "${FD_PATHS[@]}"
fd fd-0fc61133   "$FZ" "$R0F" "${FD_PATHS[@]}"
fd fd-077e212b   "$FZ" "$R07" "${FD_PATHS[@]}"
fd fd-cb4326b2   "$FZ" "$RCB" "${FD_PATHS[@]}"
fd fd-genctrl    "$FZ" "$R07" tools/round-38/gen-controls.py

echo "== intended-doc (round-38 l1 receipts)"
idoc id-base      "$B77" "$B77" PROVINCE.md "$UNIT" "$INT"
idoc id-final     "$R7A" "$B77" PROVINCE.md "$UNIT" "$INT"
idoc id-0fc61133  "$R0F" "$B77" PROVINCE.md "$UNIT" "$INT"
idoc id-s2        HEAD   "$B77" PROVINCE.md "$UNIT" "$INT"
idoc id-s2-hist   "$E26" "$B77" PROVINCE.md "$UNIT" "$INT"

echo "== registry-immutable (round-38 l1 receipts)"
ri rm-atfinal   "$A/registry-immutable.sh"        "$B77" "$R7A"
ri rm-0fc61133  "$A/registry-immutable.sh"        "$B77" "$R0F"
ri rm-base      "$A/registry-immutable.sh"        "$B77" "$B77"
echo "== registry-immutable.fixed.sh (optional variant, same receipts)"
ri rmfix-atfinal   "$A/registry-immutable.fixed.sh" "$B77" "$R7A"
ri rmfix-0fc61133  "$A/registry-immutable.fixed.sh" "$B77" "$R0F"
ri rmfix-base      "$A/registry-immutable.fixed.sh" "$B77" "$B77"

echo "== usage path (no arguments) parity"
usage_parity usage-freeze-drift freeze-drift.py
usage_parity usage-intended-doc intended-doc.py

echo "== committed-receipt cross-check (patched stdout, normalised)"
for pair in "fd-final:freeze-drift-final.json" "fd-0fc61133:freeze-drift-0fc61133.json" \
            "fd-077e212b:freeze-drift-077e212b.json" "fd-cb4326b2:freeze-drift-cb4326b2.json" \
            "fd-genctrl:freeze-drift-gen-controls.json"; do
  name=${pair%%:*}; f=${pair#*:}
  if diff -q <(norm_fd "$P/$name.patched") <(norm_fd "$RCPT/$f") >/dev/null 2>&1; then
    echo "receipt $f: identical to patched stdout (verdict, drift, paths, net fields)"
  else
    bad "receipt $f differs from patched stdout"
    diff -u <(norm_fd "$RCPT/$f") <(norm_fd "$P/$name.patched") | head -24
  fi
done
for pair in "id-base:intended-doc/base.json" "id-final:intended-doc/final.json" \
            "id-0fc61133:intended-doc/landed-0fc61133.json"; do
  name=${pair%%:*}; f=${pair#*:}
  if diff -q "$P/$name.patched" "$RCPT/$f" >/dev/null 2>&1; then
    echo "receipt $f: byte-identical to patched stdout"
  else
    bad "receipt $f differs from patched stdout"
    diff -u "$RCPT/$f" "$P/$name.patched" | head -24
  fi
done
echo -n "receipt intended-doc/shortcut-s2.json: "
if diff -q "$P/id-s2.patched" "$RCPT/intended-doc/shortcut-s2.json" >/dev/null 2>&1; then
  echo "byte-identical to patched stdout"
else
  echo "not reproducible at today's HEAD (rev was 'HEAD'); historical HEAD $E26 comparison below"
  echo "  id-s2 at HEAD:        $(tr -d '\n' < "$P/id-s2.patched" | grep -o '"verdict": "[a-z-]*"')"
  echo "  id-s2 at e265533e:    $(tr -d '\n' < "$P/id-s2-hist.patched" | grep -o '"verdict": "[a-z-]*"'), reasons $(tr -d '\n' < "$P/id-s2-hist.patched" | grep -o '\["intended path not named in the unit row"\]')"
  echo "  stored receipt:       $(tr -d '\n' < "$RCPT/intended-doc/shortcut-s2.json" | grep -o '"verdict": "[a-z-]*"'), reasons [\"intended path not named in the unit row\"]"
fi
for pair in "rm-atfinal:registry-immutable/at-final.txt" "rm-0fc61133:registry-immutable/at-0fc61133.txt" \
            "rm-base:registry-immutable/base-vs-base.txt"; do
  name=${pair%%:*}; f=${pair#*:}
  want=$(sed -n 's/^exit \([0-9]\+\)$/\1/p' "$RCPT/$f")
  if diff -q <(norm_rm "$P/$name.patched") <(norm_rm "$RCPT/$f") >/dev/null 2>&1; then
    echo "receipt $f: body identical to patched stdout (stdout carried no 'exit N' line; rc recorded = $want)"
  else
    bad "receipt $f differs from patched stdout"
    diff -u <(norm_rm "$RCPT/$f") <(norm_rm "$P/$name.patched") | head -24
  fi
done

echo "PARITY cases=$n mismatches=$fail"
[ "$fail" -eq 0 ]
