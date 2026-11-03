#!/bin/sh
# Prospective candidate only: independent review + explicit gate adoption required.
# Preserve original prefile command; this version does not claim it passed.
set -u
[ "$#" -eq 1 ] || exit 2
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
root=$1
fail=0
out=$(GIT_OPTIONAL_LOCKS=0 git -C "$root" status --porcelain) || exit 2
if [ -n "$out" ]; then
    printf '%s\n' "$out"
    echo 'prefile-reconciliation-v1: tree NOT CLEAN'; fail=1
else echo 'prefile-reconciliation-v1: tree clean'; fi
rev=$(git -C "$root" rev-parse HEAD) || exit 2
python3 -I -B "$root/tools/ledger-reconciliation-v1/gate.py" --root "$root" --rev "$rev"
rc=$?
echo "prefile-reconciliation-v1: prospective ledger reconciliation exit=$rc"
[ "$rc" -eq 0 ] || fail=1
# Retain the existing active v2 leg, with no change to its matching semantics.
if git -C "$root" cat-file -e "$rev:corpus/claim-freezes-v2.tsv" 2>/dev/null; then
    python3 -I -B "$root/tools/round-29/freeze-gate.py" --root "$root" --rev "$rev" --disclosures corpus/claim-freezes-v2.tsv
    rc=$?
    echo "prefile-reconciliation-v1: active v2 ledger exit=$rc"
    [ "$rc" -eq 0 ] || fail=1
fi
[ "$fail" -eq 0 ] && echo 'prefile-reconciliation-v1: PASS (prospective only)' || echo 'prefile-reconciliation-v1: FAIL'
exit "$fail"
