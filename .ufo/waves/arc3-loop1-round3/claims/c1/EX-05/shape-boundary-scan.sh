#!/usr/bin/env bash
# shape-boundary-scan.sh — seat EX-05 (chain c1, round 3).
# Falsifiable follow-up to the shape census: is the GT-root binary-search
# dispatcher a function of the OPTIMIZER, or of the SELECTOR COUNT?
# Generates a synthetic contract with N external functions, compiles it in both
# optimizer modes with the receipted solc, and classifies the dispatcher shape.
# Scratch under /var/tmp (host /tmp is EDQUOT).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
PREFIX="$REPO/.ufo/waves/arc3-loop1-round1/tools/solc-prefix"
SCAN=/var/tmp/ex05-shape
D="$REPO/.ufo/waves/arc3-loop1-round3/claims/c1/EX-05"
mkdir -p "$SCAN"
export TMPDIR="$SCAN/tmp"; mkdir -p "$TMPDIR"

printf '%-4s %-6s %-8s %-8s %-6s %-8s\n' N mode bytes shape eq gt
for N in 4 5 6 7 8 9 10 11 12; do
  SRC="$SCAN/Shape$N.sol"
  {
    echo '// SPDX-License-Identifier: MIT'
    echo 'pragma solidity =0.8.37;'
    echo "contract Shape$N {"
    for i in $(seq 0 $((N-1))); do
      echo "    function f$i() external view returns (uint256) { return $i; }"
    done
    echo '}'
  } > "$SRC"
  for mode in opt200 nopt; do
    OUT="$SCAN/Shape$N-$mode"
    mkdir -p "$OUT"
    node - "$PREFIX" "$SRC" "$OUT" "Shape$N" "$mode" <<'JS'
const fs = require('fs');
const [, , prefix, src, out, name, mode] = process.argv;
const solc = require(prefix + '/node_modules/solc');
const input = {
  language: 'Solidity',
  sources: { [`${name}.sol`]: { content: fs.readFileSync(src, 'utf8') } },
  settings: {
    optimizer: mode === 'opt200' ? { enabled: true, runs: 200 } : { enabled: false },
    outputSelection: { '*': { '*': ['evm.deployedBytecode.object'] } },
  },
};
const o = JSON.parse(solc.compile(JSON.stringify(input)));
const c = o.contracts[`${name}.sol`][name];
fs.writeFileSync(out + '/runtime.hex', c.evm.deployedBytecode.object + '\n');
JS
    python3 "$D/dispatch-shape.py" "$OUT/runtime.hex" | awk -v n="$N" -v m="$mode" '
      /bytes=/ { split($1,b,"="); split($2,s,"="); printf "%-4s %-6s %-8s %-8s", n, m, b[2], s[2] }
      /eq=/ { split($1,e,"="); split($2,g,"="); split($3,l,"="); printf " %-6s %-8s\n", e[2], g[2] }'
  done
done