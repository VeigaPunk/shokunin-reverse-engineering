#!/bin/bash
# driver for R45W2PreflightReal attacks
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$L/.ufo/waves/round-45/w2/R45W2PreflightReal
cd "$L" || exit 3
: > "$R/exits.tsv"
date -u +%Y-%m-%dT%H:%M:%SZ > "$R/started-utc.txt"
run() {
  name=$1
  shift
  utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  python3 -I -B tools/round-45/frozen-path-preflight.py --root "$L" "$@" > "$R/$name.stdout" 2> "$R/$name.stderr"
  rc=$?
  sha=$(sha256sum "$R/$name.stdout" | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$sha" "$utc" >> "$R/exits.tsv"
  echo "RUN $name rc=$rc sha=$sha"
}
run a1-r44-pathspec --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures/ --freeze-path tools/round-44/control-fixtures --require-pathspec
run a2-r45-clean --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty
run a3-r44-whole-tree --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --freeze-path tools/round-44/control-fixtures
date -u +%Y-%m-%dT%H:%M:%SZ > "$R/finished-utc.txt"
cat "$R/exits.tsv"
