#!/bin/sh
# R39-C1 carrier K6 — development check. sasquatch-v4be ONLY.
# NEVER run rea-agents `extract-firmware` or unblob against this carrier before
# the round-39 freeze: K6 must reach REA for the first time in the after-run.
#
# usage: ./dev-check.sh [CARRIER]
# Verifies (1) the -lls listing, (2) an extraction with the exact argument
# vector unblob's SquashFSExtractor builds for a non-AVM big-endian v4 image,
# (3) every oracle.tsv regular file (sha256 + size) and every symlinks.tsv
# link target/class against that extraction.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
C=${1:-$here/carrier.sqsh}
OUT=${TMPDIR:-/tmp}/k6-devcheck.$$
rm -rf -- "$OUT"
mkdir -p -- "$OUT"
trap 'rm -rf -- "$OUT"' EXIT

echo "# sasquatch-v4be -be -lls $C"
sasquatch-v4be -be -lls "$C"

echo "# sasquatch-v4be -be -no-exit-code -f -d $OUT/ext $C"
sasquatch-v4be -be -no-exit-code -f -d "$OUT/ext" "$C"

python3 - "$OUT/ext" "$here/oracle.tsv" "$here/symlinks.tsv" <<'PY'
import hashlib
import os
import sys

root, oracle, links = sys.argv[1:4]
bad = 0
for line in open(oracle):
    rel, want, size = line.rstrip('\n').split('\t')
    p = os.path.join(root, rel)
    if os.path.islink(p) or not os.path.isfile(p):
        print('NOT-REGULAR', rel)
        bad += 1
        continue
    data = open(p, 'rb').read()
    ok = hashlib.sha256(data).hexdigest() == want and len(data) == int(size)
    print(('OK  ' if ok else 'FAIL'), rel, len(data))
    bad += 0 if ok else 1
for line in open(links):
    rel, target, cls = line.rstrip('\n').split('\t')
    p = os.path.join(root, rel)
    got = os.readlink(p) if os.path.islink(p) else None
    ok = got == target
    print(('OK  ' if ok else 'FAIL'), 'link', rel, '->', got, cls)
    bad += 0 if ok else 1
print('bad =', bad)
sys.exit(1 if bad else 0)
PY
