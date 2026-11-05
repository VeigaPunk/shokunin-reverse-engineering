#!/bin/sh
# ConnectorOverlap receipt: cites exact lines of corpus/README.md, SCORECARD.md and lessons at the Bk clone.
set -u
C="$1"
cd "$C" || exit 2
test "$(git rev-parse --show-toplevel)" = "$C" || exit 3
echo "HEAD $(git rev-parse HEAD)"
echo "== frontier clauses PE/Mach-O (corpus/README.md)"
for n in 349 351 382 384 387 389 391 395 397 399 401 403 405 407; do printf '%s: ' "$n"; sed -n "${n}p" corpus/README.md | cut -c1-150; done
echo "== coverage rows 134-141 (verdict head)"
for n in 134 135 136 137 138 139 140 141; do printf '%s: ' "$n"; sed -n "${n}p" corpus/README.md | cut -c1-150; done
echo "== SCORECARD round headers 93-97"
for n in 6622 6644 6666 6687 6711; do printf '%s: ' "$n"; sed -n "${n}p" SCORECARD.md | cut -c1-150; done
echo "== lesson verdict lines"
sed -n '21p;31p' corpus/lessons/round-93-verifier-spotcheck.md | cut -c1-150
sed -n '29p;54p' corpus/lessons/round-94-verifier-spotcheck.md | cut -c1-150
sed -n '45p;79p' corpus/lessons/round-95-verifier-spotcheck.md | cut -c1-150
sed -n '21p;34p' corpus/lessons/round-96-verifier-spotcheck.md | cut -c1-150
sed -n '24p;35p' corpus/lessons/round-97-verifier-spotcheck.md | cut -c1-150
echo "== lessons index header lines 288-295 present (round labels)"
sed -n '291p;292p;293p' corpus/README.md | cut -c1-40
exit 0
