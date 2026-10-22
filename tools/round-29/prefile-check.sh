#!/bin/sh
# Pre-file gate (mistakes M29-1, M29-2, M29-4): run on the lane after the last seat has settled and
# the last lane commit has landed, before the round report is filed. Read-only: it runs no git
# write, and GIT_OPTIONAL_LOCKS=0 keeps `git status` from refreshing the index (LOG.md round 27).
#
#   1. tree     `git status --porcelain` is empty (no modified, staged or untracked path);
#   2. ledger   the round-24 freeze gate (.ufo/waves/round-24/tools/freeze-gate.py in the target
#               tree) with --disclosures corpus/claim-freezes.tsv exits 0 at HEAD;
#   3. ledger2  when the target tree holds corpus/claim-freezes-v2.tsv, the round-29 gate (the
#               freeze-gate.py next to this script) with --disclosures on it exits 0 at HEAD.
#
# It cannot see whether a dispatched seat is still running: that is checked in the session (the
# L1's job listing) and recorded in the report. Exit 0 when every step passes, 1 when any fails
# (each failure is printed), 2 on usage or when git cannot read the tree.
[ $# -eq 1 ] || { echo "usage: prefile-check.sh <lane-root>" >&2; exit 2; }
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
root=$1
here=$(cd "$(dirname "$0")" && pwd)
fail=0
out=$(GIT_OPTIONAL_LOCKS=0 git -C "$root" status --porcelain) || exit 2
if [ -n "$out" ]; then
    printf '%s\n' "$out"
    echo "prefile: tree NOT CLEAN ($(printf '%s\n' "$out" | wc -l) paths)"
    fail=1
else
    echo "prefile: tree clean"
fi
rev=$(git -C "$root" rev-parse HEAD) || exit 2
old="$root/.ufo/waves/round-24/tools/freeze-gate.py"
if [ -f "$old" ]; then
    python3 -I -B "$old" --root "$root" --rev "$rev" --disclosures corpus/claim-freezes.tsv > /dev/null
    rc=$?
    echo "prefile: round-24 gate --disclosures corpus/claim-freezes.tsv at $rev exit=$rc"
    [ "$rc" -eq 0 ] || fail=1
else
    echo "prefile: round-24 gate absent in the target tree"
    fail=1
fi
if git -C "$root" cat-file -e "$rev:corpus/claim-freezes-v2.tsv" 2>/dev/null; then
    python3 -I -B "$here/freeze-gate.py" --root "$root" --rev "$rev" --disclosures corpus/claim-freezes-v2.tsv > /dev/null
    rc=$?
    echo "prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at $rev exit=$rc"
    [ "$rc" -eq 0 ] || fail=1
fi
[ "$fail" -eq 0 ] && echo "prefile: PASS" || echo "prefile: FAIL"
exit "$fail"
