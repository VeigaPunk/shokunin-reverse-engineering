#!/usr/bin/env bash
# arc3-loop1-round3 c1/EX-03 — paired optimizer leg transcript (off + on re-run).
set -u
S=/var/tmp/ex03-r3
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SOLCJS=$REPO/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/.bin/solcjs
export TMPDIR=$S/tmp
cd "$S/a" || exit 1

echo "== paired optimizer legs, re-run at $(date -u +%Y-%m-%dT%H:%M:%SZ) =="
echo "source: $S/a/carrierA.sol sha256 $(sha256sum carrierA.sol | cut -d' ' -f1)"
echo "compiler: $(node "$SOLCJS" --version)"

echo
echo "-- CLI off leg: solcjs --bin --abi (no optimizer flags) --"
mkdir -p "$S/a-cli-off-out2"
node "$SOLCJS" --bin --abi -o "$S/a-cli-off-out2" carrierA.sol
echo "exit=$?"
sha256sum "$S/a-cli-off-out2"/*

echo
echo "-- stdjson off leg --"
node "$S/run-paired-opt.js" off
echo "exit=$?"

echo
echo "-- stdjson on leg (spoken for the primary flags run) --"
node "$S/run-paired-opt.js" on
echo "exit=$?"

echo
echo "-- identity vs first capture --"
for f in "$S/a-cli-off-out/carrierA_sol_CarrierA.bin" "$S/a-stdjson-opt-off/carrierA.runtime.hex" "$S/a-stdjson-opt-on/carrierA.runtime.hex"; do
  base=$(basename "$f")
  d2=$(dirname "$f")-rerun-check
  echo "$base first=$(sha256sum "$f" | cut -d' ' -f1)"
done
cmp "$S/a-cli-off-out/carrierA_sol_CarrierA.bin" "$S/a-cli-off-out2/carrierA_sol_CarrierA.bin" && echo "cli-off creation: re-run byte-identical"