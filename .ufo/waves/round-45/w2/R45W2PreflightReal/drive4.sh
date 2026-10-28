#!/bin/bash
# c1/c2: does the covers() guard agree with the git pathspec semantics actually used?
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$L/.ufo/waves/round-45/w2/R45W2PreflightReal
cd "$L" || exit 3
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
# c1: not_covered_by_string test
run c1a-decoy-sibling-pathspec --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures-extra/ --freeze-path tools/round-44/control-fixtures --require-pathspec
# c2: guard satisfied by the parent string, scanner narrowed by an exclude pathspec (pos/ holds six of the eight)
run c2a-cover-plus-exclude --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --pathspec tools/round-44/control-fixtures/ --pathspec ':(exclude)tools/round-44/control-fixtures/pos/' --freeze-path tools/round-44/control-fixtures --require-pathspec
cat "$R/exits.tsv" | tail -2
