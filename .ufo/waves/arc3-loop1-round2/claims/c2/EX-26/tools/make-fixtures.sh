#!/bin/bash
# EX-26 timing-fixture builder (reproduce the scaling/fail-closure roots).
# Writes only under /var/tmp/ex26 (repo rule: scratch outside /tmp).
set -u
SRC=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
BASE=/var/tmp/ex26
mkdir -p "$BASE"

# fx-absent: SKILL.md missing (H1 silent-PASS fixture; PROVINCE/SCORECARD present)
rm -rf "$BASE/fx-absent"; mkdir -p "$BASE/fx-absent"
cp "$SRC/PROVINCE.md" "$SRC/SCORECARD.md" "$BASE/fx-absent/"

# fx-Nx: the three scoped files padded with locus-free filler to N x their lines
for M in 8 32; do
  rm -rf "$BASE/fx-${M}x"; mkdir -p "$BASE/fx-${M}x"
  python3 - "$SRC" "$BASE/fx-${M}x" "$M" <<'PY'
import os, sys
src, dst, mult = sys.argv[1], sys.argv[2], int(sys.argv[3])
for f in ("PROVINCE.md", "SCORECARD.md", "SKILL.md"):
    lines = open(os.path.join(src, f), encoding="utf-8").read().splitlines(True)
    n = len(lines)
    with open(os.path.join(dst, f), "w", encoding="utf-8") as fh:
        fh.writelines(lines)
        fh.writelines("filler padding line %06d of the ex26 scaling fixture\n" % i
                      for i in range(n * (mult - 1)))
PY
done

# fx-32x-absent: same 32x root with SKILL.md removed (guard-at-scale fixture)
rm -rf "$BASE/fx-32x-absent"; cp -r "$BASE/fx-32x" "$BASE/fx-32x-absent"
rm "$BASE/fx-32x-absent/SKILL.md"

wc -l "$BASE"/fx-8x/* "$BASE"/fx-32x/* "$BASE"/fx-absent/* 2>/dev/null
