#!/bin/bash
# EX-22 (chain c3, arc3-loop1-round4) — before-state reproduction of the three C3
# residuals, on /var/tmp copies of the CURRENT custody tool. No custody path is written.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ROOT=/var/tmp/ex22-baseline
TOOL=$ROOT/tool/custody-pair.py
W=$ROOT/work
TR=$ROOT/transcripts
rm -rf "$W" "$TR"
mkdir -p "$ROOT/tool" "$W/a" "$W/b" "$W/c" "$TR"
cp "$REPO/.ufo/gates/custody-pair/custody-pair.py" "$TOOL"

cat > "$ROOT/build_dupe.py" <<'PY'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
t = pathlib.Path(src).read_text()
i = t.index("PATH:")
head, stanza = t[:i], t[i:]
body = head + stanza * 5
pathlib.Path(dst).write_text(body)
print("built %s: PATH-stanzas=%d" % (dst, body.count("PATH:")))
PY

r() {
  local name=$1; shift
  local log="$TR/$name.txt"
  { echo "\$ $*"; "$@"; echo "[exit-status] $?"; } >"$log" 2>&1
  echo "== $name =="
  cat "$log"
  echo
}

echo "############ 0. identity ############"
r 0a-date date -u '+%Y-%m-%dT%H:%M:%SZ'
r 0b-host hostname
r 0c-id id
r 0d-kernel uname -r
r 0e-python python3 --version
r 0f-head git -C "$REPO" rev-parse HEAD
r 0g-head-blob bash -c "cd $REPO && git cat-file -p HEAD:.ufo/gates/custody-pair/custody-pair.py | sha256sum"
r 0h-status git -C "$REPO" status --porcelain -- .ufo/gates/custody-pair/
r 0i-real-tool-sha sha256sum "$REPO/.ufo/gates/custody-pair/custody-pair.py"
r 0j-copy-sha sha256sum "$TOOL"
r 0k-stat stat -c 'name=%n size=%s mode=%a mtime=%Y inode=%i' "$REPO/.ufo/gates/custody-pair/custody-pair.py"
r 0l-cmp cmp "$REPO/.ufo/gates/custody-pair/custody-pair.py" "$TOOL"

echo "############ (a) sidecar-scope injection ############"
printf '1111111111111111111111111111111111111111111111111111111111111111  vic\n' > "$W/a/vic.sha256"
r a0-fixture-ls ls -la "$W/a"
r a0b-fixture-cat cat "$W/a/vic.sha256"
r a0c-fixture-sha sha256sum "$W/a/vic.sha256"
r a1-inject-paths-sidecar-out-measured-base python3 "$TOOL" capture --paths "$W/a/vic.sha256" --out "$W/a/vic"
r a2-after-ls ls -la "$W/a"
r a2b-after-cat cat "$W/a/vic.sha256"
r a2c-after-sha sha256sum "$W/a/vic.sha256"
r a2d-after-stat stat -c 'name=%n size=%s mode=%a inode=%i mtime=%Y ctime=%Z' "$W/a/vic.sha256"
r a3-consequence-verify-live python3 "$TOOL" verify "$W/a/vic" --live

printf 'NEIGHBOUR-ORIGINAL\n' > "$W/a/vic2"
printf '2222222222222222222222222222222222222222222222222222222222222222  vic2\n' > "$W/a/vic2.sha256"
r a4-fixture2-sha sha256sum "$W/a/vic2" "$W/a/vic2.sha256"
r a5-inject2-same-shape python3 "$TOOL" capture --paths "$W/a/vic2.sha256" --out "$W/a/vic2"
r a6-after2-sha sha256sum "$W/a/vic2" "$W/a/vic2.sha256"
r a6b-after2-cat-vic2 cat "$W/a/vic2"

printf '3333333333333333333333333333333333333333333333333333333333333333  vic3\n' > "$W/a/vic3.sha256"
printf 'NEIGHBOUR3-ORIGINAL\n' > "$W/a/vic3"
r a7-fixture3-sha sha256sum "$W/a/vic3" "$W/a/vic3.sha256"
r a8-inject3-out-sidecar-shaped python3 "$TOOL" capture --paths "$W/a/vic3" --out "$W/a/vic3.sha256"
r a9-after3-ls ls -la "$W/a"
r a9b-after3-sha sha256sum "$W/a/vic3" "$W/a/vic3.sha256"
r aA-control-direct-refusal python3 "$TOOL" capture --paths "$W/a/vic3" --out "$W/a/vic3"

echo "############ (b) mkdir traceback ############"
printf 'regular file\n' > "$W/b/blocker"
r b0-fixture-ls ls -la "$W/b"
r b1-mkdir-traceback python3 "$TOOL" capture --out "$W/b/blocker/sub/r.txt" --paths "$W/b/blocker"
r b2-after-ls ls -la "$W/b"
r b3-control-declared-path python3 "$TOOL" capture --out "$W/b/blocker" --paths "$W/b/blocker"
r b4-control-normal-mkdir python3 "$TOOL" capture --out "$W/b/fresh/deep/r.txt" --paths "$W/c/ref1.conf"

echo "############ (s) tool health before injections ############"
r s1-selftest python3 "$TOOL" selftest --scratch /var/tmp

echo "############ (c) duplicate-stanza gate pass ############"
for i in 1 2 3 4 5; do printf 'ref-%d\n' "$i" > "$W/c/ref$i.conf"; done
r c0-fixture-ls ls -la "$W/c"
r c1-capture-1of5 python3 "$TOOL" capture --out "$W/c/c1-rec.txt" --paths "$W/c/ref1.conf"
r c2-build-dupe python3 "$ROOT/build_dupe.py" "$W/c/c1-rec.txt" "$W/c/c1-dupe5.txt"
r c2b-dupe-stanza-count grep -c '^PATH:' "$W/c/c1-dupe5.txt"
r c3-dupe-gate-pass python3 "$TOOL" verify "$W/c/c1-dupe5.txt" --live --require-paths 5
r c4-control-1of5-gated python3 "$TOOL" verify "$W/c/c1-rec.txt" --live --require-paths 5
r c5-sums-dupe-build bash -c "SHA=\$(sha256sum $W/c/ref1.conf | cut -d' ' -f1); for i in 1 2 3 4 5; do echo \"\$SHA  $W/c/ref1.conf\"; done > $W/c/c1-sums-dupe5.txt"
r c5b-sums-dupe-cat cat "$W/c/c1-sums-dupe5.txt"
r c6-sums-dupe-gate-pass python3 "$TOOL" verify "$W/c/c1-sums-dupe5.txt" --live --require-paths 5
r c7-capture-5scratch python3 "$TOOL" capture --out "$W/c/c5-rec.txt" --paths "$W/c/ref1.conf" "$W/c/ref2.conf" "$W/c/ref3.conf" "$W/c/ref4.conf" "$W/c/ref5.conf"
r c8-unrelated-gate-pass python3 "$TOOL" verify "$W/c/c5-rec.txt" --live --require-paths 5
r c9-ex24-fixture python3 "$TOOL" verify "$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/EX-24/fixtures/v2-dupe-5x.txt" --live --require-paths 5
r cA-coverage-grep bash -c "for f in c3-dupe-gate-pass c4-control-1of5-gated c6-sums-dupe-gate-pass c8-unrelated-gate-pass c9-ex24-fixture; do echo \"\$f: REFERENCE-COVERAGE lines=\$(grep -c REFERENCE-COVERAGE $TR/\$f.txt)\"; done"

echo "############ z. identity re-derivation ############"
r z1-real-tool-sha-after sha256sum "$REPO/.ufo/gates/custody-pair/custody-pair.py"
r z2-copy-sha-after sha256sum "$TOOL"
r z3-status-after git -C "$REPO" status --porcelain -- .ufo/gates/custody-pair/
r z4-date-end date -u '+%Y-%m-%dT%H:%M:%SZ'
