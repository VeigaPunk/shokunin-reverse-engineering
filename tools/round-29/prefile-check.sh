#!/bin/sh
# Pre-file gate (mistakes M29-1, M29-2, M29-4): run on the lane after the last seat has settled and
# the last lane commit has landed, before the round report is filed. Read-only: it runs no git
# write, and GIT_OPTIONAL_LOCKS=0 keeps `git status` from refreshing the index (LOG.md round 27).
#
#   1. tree     `git status --porcelain` is empty (no modified, staged or untracked path);
#   2. ledger   retired at round 68 (erratum r68-1): the legacy corpus/claim-freezes.tsv is frozen
#               evidence and must stay byte-identical to its retirement pin (sha256 in the step);
#               the live ledger check is step 3 (ledger2) below;
#   3. ledger2  the live ledger: when the target tree holds corpus/claim-freezes-v2.tsv, the round-29
#               gate (the
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
# ledger1 (round-68 erratum r68-1; corrected round 69 under R68-V4): corpus/claim-freezes.tsv is
# RETIRED as a gate input. It carries 21 data rows whose last round is round-35 and no row for any
# round 36-68 (`awk -F'\t' 'NR>1{print $1}' corpus/claim-freezes.tsv | sort -u`), and its round-35
# row's container is claims-frozen.json, which the round-24 gate's expected set (claims.json files
# only) cannot match; the gate's disclosure receipt recorded `exact 20 of 21` at f78fc766, not a clean
# ledger. The file is kept as frozen evidence: this step asserts its bytes are identical to its
# retirement pin, and the live check is ledger2 below.
legacy_sha=2a840d72acfd71e55fc16aa614dcefee7afd0cf67e276b799ac9d41e773dda81
if git -C "$root" cat-file -e "$rev:corpus/claim-freezes.tsv" 2>/dev/null; then
    got=$(git -C "$root" show "$rev:corpus/claim-freezes.tsv" | sha256sum | cut -d' ' -f1)
    if [ "$got" = "$legacy_sha" ]; then
        echo "prefile: ledger1 retired (erratum r68-1) — legacy ledger byte-identical to its retirement pin"
    else
        echo "prefile: ledger1 legacy ledger changed (want $legacy_sha, got $got)"
        fail=1
    fi
else
    echo "prefile: ledger1 legacy ledger absent at $rev"
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
