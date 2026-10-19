#!/usr/bin/env bash
# EX-40 edge matrix for the REAL custody tool (capture/verify CLI), scratch fixtures only.
# Declared table (see edge-cases.md):
#   missing path            -> capture exit 13 ABSENT (receipt written)
#   unreadable path (EACCES)-> capture exit 14 UNEVALUABLE (receipt written, READ-ERROR)
#   exists-but-EACCES parent-> capture exit 14 UNEVALUABLE
#   symlink (ok/dangling/loop/dir/devnull) -> capture exit 0, TYPE: symlink
#   fifo / directory        -> capture exit 0, TYPE: other (never opened; no hang)
#   verify: unevaluable stanza vs live -> exit 14, never MATCH
# Usage: TOOL=/path/to/custody-pair.py edge-matrix-real.sh
set -u
T=${TOOL:?set TOOL to the custody-pair.py under test}
R=/var/tmp/ex40/fix
W=/var/tmp/ex40/matrix-$(basename "$(dirname "$T")")
rm -rf "$W"; mkdir -p "$W"
pass=0; fail=0
chk() { # chk <label> <want> <got>
  if [ "$2" = "$3" ]; then echo "OK    $1  exit=$3"; pass=$((pass+1));
  else echo "FAIL  $1  exit=$3 (declared $2)"; fail=$((fail+1)); fi
}
cap() { ( cd "$R" && timeout 10 python3 "$T" capture --out - --paths "$1" 2>&1 ); }

for pair in "good.txt 0" "missing.txt 13" "unreadable.txt 14" "blocked_dir/inner.txt 14" \
            "link_ok.txt 0" "link_dangling.txt 0" "link_loop_a 0" "link_dir 0" "link_devnull 0" \
            "pipe.fifo 0" "dir_target 0"; do
  f=${pair% *}; want=${pair#* }
  out=$(cap "$f"); rc=$?
  chk "capture $f" "$want" "$rc"
done

# TYPE checks the exit class alone does not prove
out=$(cap link_dangling.txt); echo "$out" | grep -q '^TYPE: symlink' && { echo "OK    dangling link typed symlink"; pass=$((pass+1)); } || { echo "FAIL  dangling link type"; fail=$((fail+1)); }
out=$(cap pipe.fifo); echo "$out" | grep -q '^TYPE: other' && { echo "OK    fifo typed other (not opened)"; pass=$((pass+1)); } || { echo "FAIL  fifo type"; fail=$((fail+1)); }

# aggregate: one good + one unreadable must still produce a receipt for BOTH paths
out=$( ( cd "$R" && timeout 10 python3 "$T" capture --out "$W/agg.txt" --paths good.txt unreadable.txt 2>&1 ) ); rc=$?
n=$(grep -c '^PATH: ' "$W/agg.txt" 2>/dev/null || echo 0)
chk "aggregate good+unreadable" 14 "$rc"; chk "aggregate receipt stanzas" 2 "$n"

# verify fail-closed: a path that is exists-but-EACCES must never verify MATCH
( cd "$R" && timeout 10 python3 "$T" capture --out "$W/blocked-pre.txt" --paths blocked_dir/inner.txt >/dev/null 2>&1 )
( cd "$R" && timeout 10 python3 "$T" verify "$W/blocked-pre.txt" --live >"$W/blocked-verify.out" 2>&1 ); rc=$?
chk "verify unevaluable-vs-live" 14 "$rc"
grep -q 'VERDICT: MATCH' "$W/blocked-verify.out" && { echo "FAIL  verify printed MATCH (fail-open)"; fail=$((fail+1)); } || { echo "OK    verify did not print MATCH"; pass=$((pass+1)); }

echo "MATRIX: $( [ "$fail" = 0 ] && echo PASS || echo FAIL ) pass=$pass fail=$fail  (workdir $W)"
[ "$fail" = 0 ]
