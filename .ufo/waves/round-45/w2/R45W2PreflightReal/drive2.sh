#!/bin/bash
# extra probes: flood control, extended clean revisions, frozen-bytes selftest
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$L/.ufo/waves/round-45/w2/R45W2PreflightReal
S=/fast/scratch/hyaku/kaidoku-r45/R45W2PreflightReal
export TMPDIR="$S"
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
# a4: same r44 range, a frozen path that is byte-identical across the range, whole-tree scan
run a4-r44-whole-tree-untouched-freezepath --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --rev c86ea508 --freeze-path plans/round-44-claims.md
# a5: the measured revision and HEAD, with the recommended invocation
run a5-r45-measured-rev --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev 1f4b27f82353d6544dc0c8048b3cfdadd8525d12 --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty
run a6-r45-head --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev HEAD --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec --check-dirty
# a7: r45 range, no --require-pathspec but with the pathspec (does clean survive without the guard?)
run a7-r45-no-require --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --pathspec tools/round-45/ --freeze-path tools/round-45 --check-dirty
# a8: frozen interpreter selftest, from the frozen blob (byte-identical copy in scratch)
git cat-file blob f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/frozen-path-preflight.py > "$S/frozen-preflight.py"
sha256sum "$S/frozen-preflight.py" "$L/tools/round-45/frozen-path-preflight.py"
utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 -I -B "$S/frozen-preflight.py" --selftest > "$R/a8-selftest.stdout" 2> "$R/a8-selftest.stderr"
rc=$?
sha=$(sha256sum "$R/a8-selftest.stdout" | cut -d' ' -f1)
printf '%s\t%s\t%s\t%s\n' "a8-selftest" "$rc" "$sha" "$utc" >> "$R/exits.tsv"
echo "RUN a8-selftest rc=$rc sha=$sha"
cat "$R/exits.tsv"
