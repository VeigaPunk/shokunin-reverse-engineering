#!/bin/bash
# b1: the two-pathspec invocation block 22 prescribes for this round's freeze
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$L/.ufo/waves/round-45/w2/R45W2PreflightReal
cd "$L" || exit 3
utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 -I -B tools/round-45/frozen-path-preflight.py --root "$L" \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 \
  --pathspec tools/round-45/ --pathspec plans/round-45-claims.md \
  --freeze-path tools/round-45 --freeze-path plans/round-45-claims.md \
  --require-pathspec --check-dirty > "$R/b1-r45-two-pathspec.stdout" 2>"$R/b1-r45-two-pathspec.stderr"
rc=$?
sha=$(sha256sum "$R/b1-r45-two-pathspec.stdout" | cut -d' ' -f1)
printf '%s\t%s\t%s\t%s\n' "b1-r45-two-pathspec" "$rc" "$sha" "$utc" >> "$R/exits.tsv"
echo "RUN b1 rc=$rc sha=$sha"
cat "$R/b1-r45-two-pathspec.stdout"
