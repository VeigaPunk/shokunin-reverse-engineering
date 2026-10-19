#!/bin/bash
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ROOT=/var/tmp/ex22-baseline
TOOL=$ROOT/tool/custody-pair.py
W=$ROOT/work
TR=$ROOT/transcripts
mkdir -p "$W/live"
r() { local name=$1; shift; local log="$TR/$name.txt"; { echo "\$ (cwd=$PWD) $*"; "$@"; echo "[exit-status] $?"; } >"$log" 2>&1; echo "== $name =="; cat "$log"; echo; }
cd "$REPO"

echo "############ live pair (READ-ONLY over custody paths; receipts to scratch) ############"
r l1-capture-pre python3 "$TOOL" capture --out "$W/live/pre.txt" --label "arc3-loop1-round4 EX-22 pre (read-only)"
r l2-capture-post python3 "$TOOL" capture --out "$W/live/post.txt" --label "arc3-loop1-round4 EX-22 post (read-only)"
r l3-verify-pair python3 "$TOOL" verify "$W/live/pre.txt" "$W/live/post.txt" --require-paths 5
r l4-verify-pre-live python3 "$TOOL" verify "$W/live/pre.txt" --live --require-paths 5
r l5-sidecar-check bash -c "cd $W/live && sha256sum -c pre.txt.sha256 && sha256sum -c post.txt.sha256"
r l6-pre-header head -20 "$W/live/pre.txt"
r l7-paths-grep grep -c '^PATH:' "$W/live/pre.txt"

echo "############ (a) rerun with repo cwd for clean receipt provenance ############"
printf 'AAAA-ORIGINAL\n' > "$W/a/vr.sha256"
r a1r-inject-repo-cwd python3 "$TOOL" capture --paths "$W/a/vr.sha256" --out "$W/a/vr"
r a1r-after-cat cat "$W/a/vr.sha256"
r a1r-after-sha sha256sum "$W/a/vr.sha256"
r a1r-receipt-head head -14 "$W/a/vr"

echo "############ (c) rerun with repo cwd + EX-24 v1 fixture ############"
printf 'ref-A\n' > "$W/c/refA.conf"
r c1r-capture-1of5-repo python3 "$TOOL" capture --out "$W/c/c1r-rec.txt" --paths "$W/c/refA.conf"
r c2r-build-dupe python3 "$ROOT/build_dupe.py" "$W/c/c1r-rec.txt" "$W/c/c1r-dupe5.txt"
r c3r-dupe-gate-pass python3 "$TOOL" verify "$W/c/c1r-dupe5.txt" --live --require-paths 5
r c3r2-grep-coverage bash -c "grep -c REFERENCE-COVERAGE $TR/c3r-dupe-gate-pass.txt || true"
r cD-ex24-v1-dupe python3 "$TOOL" verify "$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/EX-24/fixtures/v1-dupe-5x.txt" --live --require-paths 5
r cE-canonical-1of5-capture python3 "$TOOL" capture --out "$W/c/bashrc-rec.txt" --paths ~/.bashrc
r cF-canonical-1of5-padded bash -c "python3 $ROOT/build_dupe.py $W/c/bashrc-rec.txt $W/c/bashrc-dupe5.txt"
r cG-canonical-padded-gate python3 "$TOOL" verify "$W/c/bashrc-dupe5.txt" --live --require-paths 5
r cH-canonical-1of5-gated-control python3 "$TOOL" verify "$W/c/bashrc-rec.txt" --live --require-paths 5

echo "############ z2. re-derivation ############"
r z9-tool-sha-final sha256sum "$REPO/.ufo/gates/custody-pair/custody-pair.py"
r zA-copy-sha-final sha256sum "$TOOL"
r zB-head-final git rev-parse HEAD
r zC-status-final git status --porcelain -- .ufo/gates/custody-pair/
r zD-parent-head git -C /home/vgpnk/Projects/shokunin rev-parse HEAD
r zE-date-final date -u '+%Y-%m-%dT%H:%M:%SZ'
