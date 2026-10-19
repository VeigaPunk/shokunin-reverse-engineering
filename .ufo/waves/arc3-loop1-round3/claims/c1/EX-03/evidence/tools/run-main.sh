#!/usr/bin/env bash
# arc3-loop1-round3 c1/EX-03 — carrier A CLI compile legs (primary flags form)
set -u
S=/var/tmp/ex03-r3
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SOLCJS=$REPO/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/.bin/solcjs
export TMPDIR=$S/tmp
A=$S/a
mkdir -p "$S/a-out" "$S/a-out2" "$S/a-stdjson-out" "$S/tmp"
cd "$A" || exit 1

echo "== host =="
date -u +"captured-at %Y-%m-%dT%H:%M:%SZ"
uname -srm
node --version

echo "== source (carrier A) =="
sha256sum "$A/carrierA.sol"
wc -c < "$A/carrierA.sol"

echo "== compiler =="
node "$SOLCJS" --version
node -e "console.log('solc pkg version:', require('$REPO/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/solc/package.json').version)"

echo "== leg 1 (PRIMARY): flags form =="
echo "cmd: node <prefix>/node_modules/.bin/solcjs --bin --abi --optimize --optimize-runs 200 -o $S/a-out carrierA.sol   (cwd=$A, TMPDIR=$S/tmp)"
node "$SOLCJS" --bin --abi --optimize --optimize-runs 200 -o "$S/a-out" carrierA.sol >"$S/a-out/stdout.txt" 2>"$S/a-out/stderr.txt"
echo "leg1 exit=$?"
echo "--- leg1 stdout (verbatim) ---"
cat "$S/a-out/stdout.txt"
echo "--- leg1 stderr (verbatim) ---"
cat "$S/a-out/stderr.txt"
echo "--- leg1 outputs ---"
ls -la "$S/a-out"
sha256sum "$S/a-out"/*

echo "== leg 1 rerun (determinism re-derivation, separate outdir) =="
node "$SOLCJS" --bin --abi --optimize --optimize-runs 200 -o "$S/a-out2" carrierA.sol >"$S/a-out2/stdout.txt" 2>"$S/a-out2/stderr.txt"
echo "leg1-rerun exit=$?"
sha256sum "$S/a-out2"/*
cmp "$S/a-out/carrierA_sol_CarrierA.bin" "$S/a-out2/carrierA_sol_CarrierA.bin" && echo "RERUN: creation bin byte-identical"
cmp "$S/a-out/carrierA_sol_CarrierA.abi" "$S/a-out2/carrierA_sol_CarrierA.abi" && echo "RERUN: abi byte-identical"

echo "== --bin-runtime flag probe (measured: unsupported) =="
node "$SOLCJS" --bin-runtime --optimize --optimize-runs 200 -o "$S/a-rtprobe" carrierA.sol 2>&1 | head -2
echo "bin-runtime probe exit=${PIPESTATUS[0]}"

echo "== done =="
date -u +"finished-at %Y-%m-%dT%H:%M:%SZ"